import os
import requests
import glob
from pathlib import Path
from typing import List, Optional
import urllib3
import json
from datetime import datetime, timezone
import jwt
import random
import string
import sys

# Disable SSL warnings if needed
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class DICOMSTOWClient:
    def __init__(self, client_id: str, client_secret: str, auth_url: str, stow_url: str):
        self.client_id = client_id
        self.client_secret = client_secret
        self.auth_url = auth_url
        self.stow_url = stow_url
        self.access_token = None
        
        # Configure session without retry strategy
        self.session = requests.Session()

    def token_expires_soon(self, buffer_seconds: int = 60) -> bool:
        """Check if the access token is about to expire"""
        if not self.access_token:
            return True
        
        decoded_payload = jwt.decode(self.access_token, options={"verify_signature": False})
        exp = decoded_payload.get("exp")
        if not exp:
            return True
        exp_utc = datetime.fromtimestamp(exp, timezone.utc).timestamp()
        current_time = datetime.now(timezone.utc).timestamp()
        return (exp_utc - current_time) < buffer_seconds
    
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
    
    def create_multipart_body(self, dicom_files: List[str]):
        """Create multipart/related body like the JavaScript version"""
        boundary = ''.join(random.choices(string.ascii_lowercase + string.digits, k=16))
        
        body_parts = []
        
        # Add each DICOM file as a separate part
        for dicom_file in dicom_files:
            with open(dicom_file, 'rb') as f:
                dicom_data = f.read()
            
            body_parts.append(f'--{boundary}\r\n'.encode())
            body_parts.append(b'Content-Type: application/dicom\r\n')
            body_parts.append(f'Content-Length: {len(dicom_data)}\r\n\r\n'.encode())
            body_parts.append(dicom_data)
            body_parts.append(b'\r\n')
        
        # Close the multipart body
        body_parts.append(f'--{boundary}--\r\n'.encode())
        
        multipart_body = b''.join(body_parts)
        content_type = f'multipart/related; type="application/dicom"; boundary={boundary}'
        
        return multipart_body, content_type
    
    def stow_dicom_files(self, dicom_files: List[str], folder_path: str) -> bool:
        """Perform STOW-RS operation for DICOM files using proper multipart/related format"""
        
        try:
            # Refresh token if needed
            if not self.get_access_token():
                print("✗ Failed to get access token")
                return False
            
            print(f"  Creating multipart body for {len(dicom_files)} DICOM files")
            
            # Create multipart body exactly like the JavaScript version
            multipart_body, content_type = self.create_multipart_body(dicom_files)
            
            headers = {
                'Content-Type': content_type,
                'Accept': 'application/dicom+json',
                'Authorization': f'Bearer {self.access_token}'
            }
            
            print(f"  Uploading {len(multipart_body)} bytes...")
            
            response = self.session.post(
                self.stow_url,
                data=multipart_body,
                headers=headers,
                verify=False,
                timeout=2000
            )
            
            print(f"  Response status: {response.status_code}")
            
            if response.status_code in [200, 201, 202]:
                print(f"✓ Successfully uploaded {len(dicom_files)} DICOM files from {folder_path}")
                return True
            else:
                print(f"✗ Failed to upload DICOM files from {folder_path}: {response.status_code}")
                if response.text:
                    print(f"  Response: {response.text[:500]}")
                return False
                
        except requests.exceptions.RequestException as e:
            print(f"✗ Error uploading DICOM files from {folder_path}: {e}")
            return False
        except Exception as e:
            print(f"✗ Unexpected error uploading DICOM files from {folder_path}: {e}")
            return False

    @staticmethod
    def find_dicom_folders(root_path: str) -> List[str]:
        """Find all folders containing .dcm files"""
        dicom_folders = []
        
        for root, dirs, files in os.walk(root_path):
            # Check if current folder contains .dcm files
            dcm_files = [f for f in files if f.lower().endswith('.dcm')]
            if dcm_files:
                dicom_folders.append(root)
        
        return dicom_folders

    @staticmethod
    def get_dicom_files_in_folder(folder_path: str) -> List[str]:
        """Get all .dcm files in a specific folder"""
        dcm_pattern = os.path.join(folder_path, "*.dcm")
        dcm_files = glob.glob(dcm_pattern, recursive=False)
        
        # Also check for uppercase extension
        dcm_pattern_upper = os.path.join(folder_path, "*.DCM")
        dcm_files.extend(glob.glob(dcm_pattern_upper, recursive=False))
        
        return dcm_files

