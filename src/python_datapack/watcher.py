# Imports
import sys
import os
import time
import threading
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler, FileSystemEvent
from .utils.print import warning

# Build processor
class BuildProcessor(threading.Thread):
	def __init__(self, build_script: str):
		super().__init__()
		self.queue: list[str] = []
		self.running = True
		self.build_script = build_script
	
	def run(self):
		while self.running:
			if len(self.queue) > 0:
				# Clear the queue and get the latest change
				latest_change = None
				while len(self.queue) > 0:
					latest_change = self.queue.pop(0)
					self.queue = []
				
				if latest_change:
					print(f"Processing changes... (Latest: {latest_change})")
					os.system(f"{sys.executable} {self.build_script}")
			
			# Wait a bit before processing more changes
			time.sleep(1)
	
	def stop(self):
		self.running = False
	
	def add_to_queue(self, file_path: str):
		self.queue.append(file_path)

# File change handler
class ChangeHandler(FileSystemEventHandler):
	def __init__(self, to_watch: list[str], to_ignore: list[str], processor: BuildProcessor):
		""" Class to handle file changes\n
		Args:
			to_watch	(list[str]):	List of paths to watch (starts with)
			to_ignore	(list[str]):	List of paths to ignore (contains)
			processor	(BuildProcessor):	Thread that processes the builds
		"""
		self.to_watch: list[str] = to_watch
		self.to_ignore: list[str] = to_ignore
		self.processor = processor
		super().__init__()

	def on_modified(self, event: FileSystemEvent):
		""" Function called when a file is modified\n
		Args:
			event	(FileSystemEvent):	Watchdog event
		"""
		source_path: str = os.path.abspath(event.src_path).replace("\\", "/")
		if not event.is_directory and not any(x in source_path for x in self.to_ignore) and any(source_path.startswith(x) for x in self.to_watch):
			self.processor.add_to_queue(source_path)

# Main watcher
def watcher(to_watch: list[str], to_ignore: list[str], build_script: str):
	""" Start a watcher to monitor file changes and automatically build the datapack\n
	Args:
		to_watch		(list[str]):	List of paths to watch (starts with)
		to_ignore		(list[str]):	List of paths to ignore (contains)
		build_script	(str):			Path to the build script
	"""
	# Start the build processor thread
	processor = BuildProcessor(build_script)
	processor.start()
	
	event_handler: ChangeHandler = ChangeHandler(to_watch, to_ignore, processor)
	observer = Observer()
	observer.schedule(event_handler, ".", recursive=True)
	observer.start()
	warning("Watching for file changes... (Press Ctrl+C to stop)")

	try:
		while True:
				observer.join(1)
	except KeyboardInterrupt:
		processor.stop()
		observer.stop()
		observer.join()
		processor.join()
	warning("Watcher stopped")
