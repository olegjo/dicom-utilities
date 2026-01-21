import os
import sys
import requests
from typing import List, Optional
from datetime import datetime, timezone

try:
    import urllib3
    # Disable SSL warnings if needed
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
except ImportError:
    urllib3 = None

try:
    import jwt
except ImportError:
    jwt = None
    print("Warning: PyJWT not installed. Token expiration checking will be disabled.")

class DICOMWADOClient:
    def __init__(self, client_id: str, client_secret: str, auth_url: str, wado_base_url: str):
        self.client_id = client_id
        self.client_secret = client_secret
        self.auth_url = auth_url
        self.wado_base_url = wado_base_url
        self.access_token = None
        
        # Configure session without retry strategy
        self.session = requests.Session()

    def token_expires_soon(self, buffer_seconds: int = 60) -> bool:
        """Check if the access token is about to expire"""
        if not self.access_token:
            return True
        
        if jwt is None:
            # If PyJWT is not available, assume token needs refresh after reasonable time
            return True
        
        try:
            decoded_payload = jwt.decode(self.access_token, options={"verify_signature": False})
            exp = decoded_payload.get("exp")
            if not exp:
                return True
            exp_utc = datetime.fromtimestamp(exp, timezone.utc).timestamp()
            current_time = datetime.now(timezone.utc).timestamp()
            return (exp_utc - current_time) < buffer_seconds
        except Exception:
            return True
    
    def get_access_token(self) -> Optional[str]:
        """Obtain access token using Client Credentials grant"""
        if self.access_token and not self.token_expires_soon():
            return self.access_token

        try:
            headers = {
                'Content-Type': 'application/x-www-form-urlencoded'
            }
            
            data = {
                'client_id': self.client_id,
                'client_secret': self.client_secret,
                'grant_type': 'client_credentials'
            }
            
            response = self.session.post(self.auth_url, headers=headers, data=data, verify=False, timeout=30)
            response.raise_for_status()
            
            token_data = response.json()
            self.access_token = token_data.get('access_token')
            
            print(f"✓ Successfully obtained access token")
            return self.access_token
            
        except requests.exceptions.RequestException as e:
            print(f"✗ Failed to obtain access token: {e}")
            return None
    
    def parse_multipart_dicom_response(self, response_content: bytes, boundary: str) -> List[bytes]:
        """Parse multipart DICOM response and extract individual DICOM files"""
        dicom_parts = []
        
        # Split by boundary
        boundary_bytes = f'--{boundary}'.encode()
        parts = response_content.split(boundary_bytes)
        
        for part in parts[1:-1]:  # Skip first empty part and last closing part
            # Find the start of DICOM data (after headers)
            header_end = part.find(b'\r\n\r\n')
            if header_end != -1:
                dicom_data = part[header_end + 4:]  # Skip the \r\n\r\n
                # Remove trailing \r\n if present
                if dicom_data.endswith(b'\r\n'):
                    dicom_data = dicom_data[:-2]
                if len(dicom_data) > 0:
                    dicom_parts.append(dicom_data)
        
        return dicom_parts
    
    def retrieve_dicom_series(self, study_uid: str, series_uid: str, output_folder: str) -> bool:
        """Perform WADO-RS operation to retrieve DICOM series"""
        
        try:
            # Refresh token if needed
            if not self.get_access_token():
                print("✗ Failed to get access token")
                return False
            
            # Construct WADO-RS URL
            wado_url = f"{self.wado_base_url}/studies/{study_uid}/series/{series_uid}"
            print(f"  Retrieving from: {wado_url}")
            
            headers = {
                'Accept': 'multipart/related; type="application/dicom"; transfer-syntax=*',
                'Authorization': f'Bearer {self.access_token}'
            }
            
            response = self.session.get(
                wado_url,
                headers=headers,
                verify=False,
                timeout=300
            )
            
            print(f"  Response status: {response.status_code}")
            
            if response.status_code == 200:
                # Parse Content-Type header to get boundary
                content_type = response.headers.get('Content-Type', '')
                boundary_start = content_type.find('boundary=')
                if boundary_start == -1:
                    print("✗ No boundary found in Content-Type header")
                    return False
                
                boundary = content_type[boundary_start + 9:].strip('"')
                print(f"  Parsing multipart response with boundary: {boundary}")
                
                # Parse multipart response
                dicom_parts = self.parse_multipart_dicom_response(response.content, boundary)
                
                if not dicom_parts:
                    print("✗ No DICOM parts found in response")
                    return False
                
                # Create output folder if it doesn't exist
                os.makedirs(output_folder, exist_ok=True)
                
                # Save each DICOM part as a file
                saved_count = 0
                for i, dicom_data in enumerate(dicom_parts):
                    filename = f"{i+1}.dcm"
                    filepath = os.path.join(output_folder, filename)
                    
                    with open(filepath, 'wb') as f:
                        f.write(dicom_data)
                    
                    saved_count += 1
                    print(f"  Saved: {filename} ({len(dicom_data)} bytes)")
                
                print(f"✓ Successfully retrieved and saved {saved_count} DICOM files to {output_folder}")
                return True
            else:
                print(f"✗ Failed to retrieve DICOM series: {response.status_code}")
                if response.text:
                    print(f"  Response: {response.text[:500]}")
                return False
                
        except requests.exceptions.RequestException as e:
            print(f"✗ Error retrieving DICOM series: {e}")
            return False
        except Exception as e:
            print(f"✗ Unexpected error retrieving DICOM series: {e}")
            return False

def parse_study_series_pairs(pairs_input: str):
    """Parse study/series UID pairs from command line input"""
    pairs = []
    
    # Split by comma or space
    pair_strings = [p.strip() for p in pairs_input.replace(',', ' ').split() if p.strip()]
    
    # Each pair should be in format "study_uid:series_uid" or "study_uid/series_uid"
    for pair_str in pair_strings:
        if ':' in pair_str:
            study_uid, series_uid = pair_str.split(':', 1)
        elif '/' in pair_str:
            study_uid, series_uid = pair_str.split('/', 1)
        else:
            print(f"⚠ Invalid pair format: {pair_str}. Expected format: study_uid:series_uid")
            continue
        
        study_uid = study_uid.strip()
        series_uid = series_uid.strip()
        
        if study_uid and series_uid:
            pairs.append((study_uid, series_uid))
        else:
            print(f"⚠ Empty UID in pair: {pair_str}")
    
    return pairs

def main():
    if len(sys.argv) < 5:
        print("Usage: python3 receive.py <base_url> <output_folder> <client_secret> <study_uid:series_uid> [study_uid2:series_uid2 ...]")
        print("Examples:")
        print("\t> python3 receive.py https://milan-workshop.eu.trials.nordicmediva.com ./output r42DJSKD8KSD8 1.2.3.4.5:1.2.3.4.6")
        print("\t> python3 receive.py https://milan-workshop.eu.trials.nordicmediva.com ./output r42DJSKD8KSD8 \"1.2.3.4.5:1.2.3.4.6 1.2.3.4.7:1.2.3.4.8\"")
        print("\t> python3 receive.py https://milan-workshop.eu.trials.nordicmediva.com ./output r42DJSKD8KSD8 1.2.3.4.5/1.2.3.4.6")
        sys.exit(-1)

    BASE_URL = sys.argv[1]
    OUTPUT_FOLDER = sys.argv[2]
    CLIENT_SECRET = sys.argv[3]
    
    # Parse study/series pairs from remaining arguments
    pairs_input = ' '.join(sys.argv[4:])
    
    # Configuration
    CLIENT_ID = "dicom-gateway-client"
    AUTH_URL = f"{BASE_URL}/auth/realms/nordicmediva/protocol/openid-connect/token"
    WADO_BASE_URL = f"{BASE_URL}/api/dicom-gateway/v1"

    print(f"Starting DICOM retrieval using WADO-RS")
    print("=" * 60)
    
    # Initialize client
    wado_client = DICOMWADOClient(CLIENT_ID, CLIENT_SECRET, AUTH_URL, WADO_BASE_URL)
    
    if not wado_client.get_access_token():
        print("✗ Cannot proceed without access token")
        return
    
    # Parse study/series pairs
    print(f"\nParsing study/series pairs...")
    study_series_pairs = parse_study_series_pairs(pairs_input)
    
    if not study_series_pairs:
        print("✗ No valid study/series pairs found")
        return
    
    print(f"✓ Found {len(study_series_pairs)} study/series pairs to retrieve")
    
    # Process each study/series pair
    successful_retrievals = 0
    failed_retrievals = 0
    
    for i, (study_uid, series_uid) in enumerate(study_series_pairs):
        print(f"\nProcessing pair {i+1}/{len(study_series_pairs)}: {study_uid}/{series_uid}")
        
        # Create output subfolder for this series
        series_folder = os.path.join(OUTPUT_FOLDER, f"study_{study_uid}", f"series_{series_uid}")
        
        # Perform WADO-RS retrieval
        if wado_client.retrieve_dicom_series(study_uid, series_uid, series_folder):
            successful_retrievals += 1
        else:
            failed_retrievals += 1
    
    # Summary
    print("\n" + "=" * 60)
    print("RETRIEVAL SUMMARY:")
    print(f"✓ Successful retrievals: {successful_retrievals}")
    print(f"✗ Failed retrievals: {failed_retrievals}")
    print(f"📁 Total study/series pairs processed: {len(study_series_pairs)}")
    print(f"📁 Output folder: {OUTPUT_FOLDER}")

if __name__ == "__main__":
    main()