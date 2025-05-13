from app import application, socketio


# Main entry point of the application
if __name__ == '__main__':
    socketio.run(application, debug=True)