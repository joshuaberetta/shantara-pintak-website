#!/usr/bin/env python3
"""
Development server with hot reloading.
Watches for changes to content.yaml and template.html, rebuilds automatically,
and serves the site with live reload.
"""

import http.server
import socketserver
import os
import sys
import time
from pathlib import Path
from threading import Thread
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from build import build_site


from pathlib import Path

PORT = 8000
PROJECT_ROOT = Path(__file__).parent.parent
WATCH_FILES = ['content.yaml', 'template.html']
DIST_DIR = str(PROJECT_ROOT / 'dist')


class BuildHandler(FileSystemEventHandler):
    """Handles file system events and triggers rebuilds."""
    
    def __init__(self):
        self.last_build = 0
        
    def on_modified(self, event):
        # Debounce rapid file changes
        if time.time() - self.last_build < 1:
            return
            
        if event.src_path.endswith(tuple(WATCH_FILES)):
            print(f"\n📝 Detected change in {Path(event.src_path).name}")
            print("🔨 Rebuilding...")
            try:
                build_site()
                self.last_build = time.time()
                print("✨ Rebuild complete! Refresh your browser.\n")
            except Exception as e:
                print(f"❌ Build error: {e}\n")


class LiveReloadHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    """HTTP request handler that serves from dist directory."""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIST_DIR, **kwargs)
    
    def end_headers(self):
        # Add headers to prevent caching during development
        self.send_header('Cache-Control', 'no-store, no-cache, must-revalidate')
        self.send_header('Expires', '0')
        super().end_headers()
    
    def log_message(self, format, *args):
        # Simplified logging
        if args[1] == '200':
            return
        super().log_message(format, *args)


def start_server():
    """Start the HTTP server."""
    with socketserver.TCPServer(("", PORT), LiveReloadHTTPRequestHandler) as httpd:
        print(f"🌍 Server running at http://localhost:{PORT}")
        print(f"👀 Watching {', '.join(WATCH_FILES)} for changes...")
        print("   Press Ctrl+C to stop\n")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n\n👋 Server stopped")
            sys.exit(0)


def start_watcher():
    """Start the file watcher."""
    event_handler = BuildHandler()
    observer = Observer()
    observer.schedule(event_handler, path=str(Path(__file__).parent), recursive=False)
    observer.start()
    return observer


def main():
    # Initial build
    print("🔨 Building site...")
    try:
        build_site()
    except Exception as e:
        print(f"❌ Initial build failed: {e}")
        sys.exit(1)
    
    print()
    
    # Start file watcher in background
    observer = start_watcher()
    
    try:
        # Start server in main thread
        start_server()
    finally:
        observer.stop()
        observer.join()


if __name__ == '__main__':
    main()
