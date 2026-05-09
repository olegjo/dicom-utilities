from pathlib import Path
from typing import List, Optional
from datetime import datetime, timezone
import sys

from DICOMSTOWClient import DICOMSTOWClient
from gitignore__destinations import destinations

def main(MEDIVA_URL, ROOT_PATH, CLIENT_SECRET):

    print(f"Using MEDIVA_URL: {MEDIVA_URL}")
    print(f"Using ROOT_PATH: {ROOT_PATH}")
    # Configuration
    CLIENT_ID = "dicom-gateway-client"
    AUTH_URL = f"{MEDIVA_URL}/auth/realms/nordicmediva/protocol/openid-connect/token"
    STOW_URL = f"{MEDIVA_URL}/api/dicom-gateway/v1/studies"

    # Current working directory
    
    print(f"Starting DICOM folder walk in: {ROOT_PATH}")
    print("=" * 60)
    
    # Initialize client
    stow_client = DICOMSTOWClient(CLIENT_ID, CLIENT_SECRET, AUTH_URL, STOW_URL)
    
    if not stow_client.get_access_token():
        print("✗ Cannot proceed without access token")
        return
    
    # Find folders containing DICOM files
    print(f"\nScanning for folders with DICOM files...")
    dicom_folders = DICOMSTOWClient.find_dicom_folders(ROOT_PATH)
    
    if not dicom_folders:
        print("✗ No folders containing DICOM files found")
        return
    
    print(f"✓ Found {len(dicom_folders)} folders containing DICOM files")
    
    # Process each folder
    successful_uploads = 0
    failed_uploads = 0
    
    for folder in dicom_folders:
        print(f"\nProcessing folder: {folder}")
        
        # Get DICOM files in this folder
        dicom_files = DICOMSTOWClient.get_dicom_files_in_folder(folder)
        
        if not dicom_files:
            print(f"⚠ No DICOM files found in {folder}")
            continue
        
        print(f"  Found {len(dicom_files)} DICOM files")
        
        # Perform STOW-RS
        if stow_client.stow_dicom_files(dicom_files, folder):
            successful_uploads += 1
        else:
            failed_uploads += 1
    
    # Summary
    print("\n" + "=" * 60)
    print("UPLOAD SUMMARY:")
    print(f"✓ Successful uploads: {successful_uploads}")
    print(f"✗ Failed uploads: {failed_uploads}")
    print(f"📁 Total folders processed: {len(dicom_folders)}")

if __name__ == "__main__":
    INSTANCE = sys.argv[1] # for example trial3
    ROOT_PATH = sys.argv[2]
    main(destinations[INSTANCE]["MEDIVA_URL"], ROOT_PATH, destinations[INSTANCE]["CLIENT_SECRET"])  