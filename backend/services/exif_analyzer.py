"""
Safe Local EXIF Metadata Inspector and Scrubber
Enables users to safely inspect what hidden data their photos leak (GPS, device model, timestamps)
and provides an in-memory scrubber to strip EXIF metadata without uploading files to external services.
Privacy by Design: Never stores user images permanently on the disk; processing is done in-memory.
"""
import io
from typing import Dict, Any, Optional
from PIL import Image, ExifTags

def _convert_to_degrees(value) -> float:
    """Helper function to convert GPS rational tuples to decimal degrees."""
    try:
        d = float(value[0])
        m = float(value[1])
        s = float(value[2])
        return d + (m / 60.0) + (s / 3600.0)
    except Exception:
        return 0.0

def inspect_image_metadata(image_bytes: bytes, filename: str = "image.jpg") -> Dict[str, Any]:
    """
    Parses EXIF metadata from raw image bytes in-memory.
    Returns structured analysis of leaked metadata points.
    """
    try:
        img = Image.open(io.BytesIO(image_bytes))
        exif_raw = img.getexif()
    except Exception as e:
        return {
            "success": False,
            "filename": filename,
            "error": f"Could not parse image: {str(e)}",
            "has_exif": False,
            "metadata": {}
        }

    if not exif_raw:
        return {
            "success": True,
            "filename": filename,
            "has_exif": False,
            "summary": "No EXIF metadata found. Photo appears clean of hardware or GPS tags.",
            "metadata": {},
            "gps": None
        }

    metadata = {}
    gps_info = {}
    
    # Standard tags
    for tag_id, value in exif_raw.items():
        tag_name = ExifTags.TAGS.get(tag_id, str(tag_id))
        # Ensure value is string-serializable
        try:
            str_val = str(value)
            # Truncate extremely long binary payloads
            if len(str_val) > 100:
                str_val = str_val[:100] + "... [truncated]"
            metadata[tag_name] = str_val
        except Exception:
            pass

    # Inspect GPS sub-IFD if present
    gps_lat = None
    gps_lon = None
    gps_raw_data = None
    try:
        # Check standard EXIF GPS IFD tag (34853)
        gps_ifd = exif_raw.get_ifd(0x8825)
        if gps_ifd:
            gps_raw_data = {}
            for t_id, t_val in gps_ifd.items():
                t_name = ExifTags.GPSTAGS.get(t_id, str(t_id))
                gps_raw_data[t_name] = str(t_val)
            
            # Extract Latitude & Longitude if present
            if "GPSLatitude" in gps_raw_data and "GPSLatitudeRef" in gps_raw_data:
                lat_vals = gps_ifd.get(2)
                lat_ref = gps_raw_data.get("GPSLatitudeRef")
                if lat_vals:
                    gps_lat = _convert_to_degrees(lat_vals)
                    if lat_ref == "S":
                        gps_lat = -gps_lat

            if "GPSLongitude" in gps_raw_data and "GPSLongitudeRef" in gps_raw_data:
                lon_vals = gps_ifd.get(4)
                lon_ref = gps_raw_data.get("GPSLongitudeRef")
                if lon_vals:
                    gps_lon = _convert_to_degrees(lon_vals)
                    if lon_ref == "W":
                        gps_lon = -gps_lon
    except Exception:
        pass

    has_gps = gps_lat is not None and gps_lon is not None
    risk_findings = []
    
    if has_gps:
        risk_findings.append({
            "severity": "CRITICAL",
            "item": f"Precise GPS coordinates exposed ({round(gps_lat, 4)}, {round(gps_lon, 4)})",
            "risk": "Anyone downloading this photo can map the exact location where it was taken."
        })
    if "DateTimeOriginal" in metadata or "DateTime" in metadata:
        risk_findings.append({
            "severity": "MEDIUM",
            "item": f"Original capture timestamp recorded: {metadata.get('DateTimeOriginal') or metadata.get('DateTime')}",
            "risk": "Reveals the exact time and date of your daily activities."
        })
    if "Make" in metadata or "Model" in metadata:
        risk_findings.append({
            "severity": "LOW",
            "item": f"Device hardware details: {metadata.get('Make', '')} {metadata.get('Model', '')}",
            "risk": "Aids device fingerprinting and physical profiling."
        })

    return {
        "success": True,
        "filename": filename,
        "has_exif": True,
        "has_gps": has_gps,
        "gps": {
            "latitude": round(gps_lat, 6) if gps_lat else None,
            "longitude": round(gps_lon, 6) if gps_lon else None,
            "map_url": f"https://www.openstreetmap.org/?mlat={gps_lat}&mlon={gps_lon}#map=16/{gps_lat}/{gps_lon}" if has_gps else None
        } if has_gps else None,
        "metadata_fields_count": len(metadata),
        "metadata": metadata,
        "risk_findings": risk_findings
    }

def strip_image_metadata(image_bytes: bytes) -> bytes:
    """
    Safely strips all EXIF, GPS, and device metadata from the image.
    Returns cleaned image bytes.
    """
    img = Image.open(io.BytesIO(image_bytes))
    
    # Create clean image buffer by copying image pixel data only
    clean_buf = io.BytesIO()
    
    # Save as PNG or JPEG without exif
    format_type = img.format if img.format in ["JPEG", "PNG", "WEBP"] else "JPEG"
    
    if img.mode in ("RGBA", "P") and format_type == "JPEG":
        img = img.convert("RGB")
        
    img.save(clean_buf, format=format_type)
    clean_buf.seek(0)
    return clean_buf.getvalue()
