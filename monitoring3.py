import time
import vdsplit3
from classifier2 import classify
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


class Watcher:
    DIRECTORY_TO_WATCH = "/home/pradnya/Downloads/EARS-master/Python_Demo/videos"

    def __init__(self):
        self.observer = Observer()

    def run(self):
        event_handler = Handler()
        self.observer.schedule(event_handler, self.DIRECTORY_TO_WATCH, recursive=True)
        self.observer.start()
        try:
            while True:
                time.sleep(5)
        except:
            self.observer.stop()
            print("Error")

        self.observer.join()


class Handler(FileSystemEventHandler):

    @staticmethod
    def on_any_event(event):
        if event.is_directory:
            flag = 0
            return None

        elif event.event_type == 'created':
            # Take any action here when a file is first created.
            print("Received created event - %s." % event.src_path)
            newVidPath = event.src_path
            ind = newVidPath.rfind("/")
            ind = ind + 1
            newVidPathLength = len(newVidPath)
            newVidName = newVidPath[ind: newVidPathLength]
            path = "frames/" + newVidName
            vdsplit3.extractFrames(newVidName, path)
            classify(path)


if __name__ == '__main__':
    w = Watcher()
    w.run()
