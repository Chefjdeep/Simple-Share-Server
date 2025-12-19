#!/usr/bin/env python3
"""
Simple Share Server - PWA Edition
Share files between devices on same WiFi
"""

import os
import sys
import socket
from flask import Flask, render_template, request, send_file, redirect, url_for, flash, jsonify, send_from_directory
from werkzeug.utils import secure_filename
import threading
import webbrowser
from datetime import datetime
import json

app = Flask(__name__)
app.secret_key = 'simple-share-secret-key-123'
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024  # 100MB max file size

# Configuration
UPLOAD_FOLDER = 'shared_files'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'mp3', 'mp4', 'zip', 'doc', 'docx', 'xls', 'xlsx'}

# Ensure upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Store uploaded file info
uploaded_files = []

def get_local_ip():
    """Get local IP address of the machine"""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return "127.0.0.1"

def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_network_info():
    """Get network information for sharing"""
    ip = get_local_ip()
    port = 5000
    return {
        'ip': ip,
        'port': port,
        'url': f"http://{ip}:{port}",
        'mobile_url': f"http://{ip}:{port}/mobile"
    }

# ========== PWA ROUTES ==========
@app.route('/manifest.json')
def serve_manifest():
    """Serve PWA manifest"""
    return send_from_directory('static', 'manifest.json')

@app.route('/service-worker.js')
def serve_service_worker():
    """Serve service worker"""
    return send_from_directory('static', 'service-worker.js')

@app.route('/static/icon-192.png')
def serve_icon_192():
    """Serve 192x192 icon"""
    return send_from_directory('static', 'icon-192.png')

@app.route('/static/icon-512.png')
def serve_icon_512():
    """Serve 512x512 icon"""
    return send_from_directory('static', 'icon-512.png')

# ========== APP ROUTES ==========
@app.route('/')
def index():
    """Main page with upload form and file list"""
    network_info = get_network_info()
    return render_template('index.html', 
                         files=uploaded_files, 
                         network=network_info,
                         allowed_extensions=', '.join(ALLOWED_EXTENSIONS))

@app.route('/mobile')
def mobile_interface():
    """Mobile-optimized PWA interface"""
    network_info = get_network_info()
    return render_template('mobile.html', 
                         files=uploaded_files[-5:],  # Last 5 files for mobile
                         network=network_info,
                         allowed_extensions=', '.join(ALLOWED_EXTENSIONS))

@app.route('/upload', methods=['POST'])
def upload_file():
    """Handle file uploads"""
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    
    files = request.files.getlist('file')
    
    for file in files:
        if file.filename == '':
            continue
            
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            
            # Save file
            file.save(filepath)
            
            # Store file info
            file_info = {
                'name': filename,
                'size': os.path.getsize(filepath),
                'upload_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'path': filepath,
                'url': f"/download/{filename}"
            }
            uploaded_files.append(file_info)
            flash(f'File {filename} uploaded successfully!')
    
    return redirect(url_for('index'))

@app.route('/mobile_upload', methods=['POST'])
def mobile_upload():
    """Handle mobile uploads with better feedback"""
    if 'file' not in request.files:
        return jsonify({'error': 'No file selected'}), 400
    
    files = request.files.getlist('file')
    uploaded = []
    
    for file in files:
        if file.filename == '':
            continue
            
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            
            # Save file
            file.save(filepath)
            
            # Store file info
            file_info = {
                'name': filename,
                'size': os.path.getsize(filepath),
                'upload_time': datetime.now().strftime('%H:%M'),
                'path': filepath,
                'url': f"/download/{filename}"
            }
            uploaded_files.append(file_info)
            uploaded.append(file_info)
    
    return jsonify({
        'success': True, 
        'message': f'Uploaded {len(uploaded)} file(s)',
        'files': uploaded
    })

@app.route('/download/<filename>')
def download_file(filename):
    """Download a file"""
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(filename))
    
    if os.path.exists(filepath):
        return send_file(filepath, as_attachment=True)
    else:
        flash('File not found')
        return redirect(url_for('index'))

@app.route('/delete/<filename>')
def delete_file(filename):
    """Delete a file"""
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(filename))
    
    if os.path.exists(filepath):
        os.remove(filepath)
        # Remove from uploaded_files list
        global uploaded_files
        uploaded_files = [f for f in uploaded_files if f['name'] != filename]
        flash(f'File {filename} deleted successfully!')
    
    return redirect(url_for('index'))

@app.route('/api/files')
def api_files():
    """API endpoint to get file list"""
    return jsonify(uploaded_files)

def open_browser():
    """Open browser automatically"""
    webbrowser.open(f"http://{get_local_ip()}:5000")

def main():
    """Main function to run the server"""
    network_info = get_network_info()
    
    print("\n" + "="*60)
    print("            SIMPLE SHARE PWA")
    print("="*60)
    print(f"📱 PWA URL: {network_info['mobile_url']}")
    print(f"💻 Desktop URL: http://localhost:5000")
    print(f"🔗 Network URL: {network_info['url']}")
    print(f"📍 IP Address: {network_info['ip']}")
    print(f"🚪 Port: {network_info['port']}")
    print("="*60)
    print("\n📲 TO INSTALL ON PHONE:")
    print("   1. Open browser on phone")
    print(f"   2. Go to: {network_info['mobile_url']}")
    print("   3. Tap 'Add to Home Screen'")
    print("   4. Use like a native app!")
    print("\n📤 Upload files from any device on same WiFi")
    print("\n🛑 Press Ctrl+C to stop the server")
    print("="*60 + "\n")
    
    # Open browser automatically
    threading.Timer(1.5, open_browser).start()
    
    # Run the server
    app.run(host='0.0.0.0', port=5000, debug=False, threaded=True)

if __name__ == '__main__':
    main()