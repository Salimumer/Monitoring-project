import psutil
import socket
import sys
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow, QStatusBar, QVBoxLayout, QWidget


class Client(QMainWindow):
    def __init__(self, ip_address):
        super().__init__()
        self.ip_address = ip_address
        self.status = QLabel("Unknown")
        self.init_ui()

    def init_ui(self):
        # Set window properties
        self.setWindowTitle(f"Client {self.ip_address}")
        self.setFixedSize(300, 100)

        # Create main widget and layout
        widget = QWidget()
        layout = QVBoxLayout(widget)

        # Add status label to layout
        label_font = QFont()
        label_font.setPointSize(24)
        self.status.setFont(label_font)
        self.status.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.status)

        # Set main widget and layout
        self.setCentralWidget(widget)

    def update_status(self, status):
        self.status.setText(status)


class Master(QMainWindow):
    def __init__(self):
        super().__init__()
        self.clients = {}
        self.init_ui()

    def init_ui(self):
        # Set window properties
        self.setWindowTitle("Master")
        self.setFixedSize(500, 500)

        # Create main widget and layout
        widget = QWidget()
        layout = QVBoxLayout(widget)

        # Add client labels to layout
        for i in range(5):
            client_label = QLabel(f"Client {i+1}: Unknown")
            layout.addWidget(client_label)
            self.clients[f"client{i+1}"] = client_label

        # Set main widget and layout
        self.setCentralWidget(widget)

        # Create status bar
        status_bar = QStatusBar()
        status_bar.showMessage("Waiting for clients...")
        self.setStatusBar(status_bar)

    def update_client_status(self, client_ip, status):
        self.clients[client_ip].setText(status)

    def update_status_bar(self, message):
        self.statusBar().showMessage(message)


class Monitor:
    def __init__(self, master_ip):
        self.master_ip = master_ip

    def is_computer_on(self):
        """Check if the computer is on or off."""
        battery = psutil.sensors_battery()
        return battery.power_plugged or battery.percent > 0

    def run(self):
        # Set up socket connection
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((self.master_ip, 1234))

        # Send data to master computer
        if self.is_computer_on():
            s.sendall(b"computer_on")
        else:
            s.sendall(b"computer_off")

        # Receive data from master computer
        data = s.recv(1024)

        # Close socket connection
        s.close()

        # Return received data
        return data.decode()


if __name__ == "__main__":
    # Create PyQt5 application
    app = QApplication(sys.argv)

    # Create master window
    master_window = Master()
    master_window.show()

    # Create client windows
    client_windows = []
    for i in range(5):
        client_window = Client(f"192.168.0.{i+1}")
        client_window.show()
        client_windows.append(client_window)

    # Start monitoring loop
    monitor = Monitor("192.168.0.100") # Replace with the IP address of the master computer
    while True:
        print("ok")
    
