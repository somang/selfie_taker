import cv2
import datetime
import os

class WebcamSelfie:
    def __init__(self):
        self.camera = None
        self.output_dir = "selfies"
        
        # Create output directory if it doesn't exist
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
    
    def initialize_camera(self, camera_index=0):
        """Initialize the webcam"""
        self.camera = cv2.VideoCapture(camera_index)
        
        if not self.camera.isOpened():
            raise ValueError("Could not open camera")
            
        # Set resolution to 1280x720
        self.camera.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        self.camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
    
    def add_overlay_text(self, frame, text, position, font_scale=1, color=(255, 255, 255)):
        """Add text overlay to the frame"""
        font = cv2.FONT_HERSHEY_SIMPLEX
        # Add black background to text for better visibility
        (text_width, text_height), _ = cv2.getTextSize(text, font, font_scale, 2)
        cv2.rectangle(frame, position, 
                     (position[0] + text_width, position[1] + text_height + 5), 
                     (0, 0, 0), -1)
        # Add text
        cv2.putText(frame, text, position, font, font_scale, color, 2)
    
    def capture_selfie(self):
        """Main function to capture selfie"""
        if self.camera is None:
            self.initialize_camera()
        
        countdown_active = False
        countdown_start = 0
        countdown_duration = 3  # seconds
        
        print("Press SPACE to start countdown and take a selfie")
        print("Press ESC to exit")
        
        while True:
            ret, frame = self.camera.read()
            if not ret:
                print("Failed to grab frame")
                break
                
            # Flip frame horizontally for natural selfie view
            frame = cv2.flip(frame, 1)
            
            if not countdown_active:
                # Show instructions
                self.add_overlay_text(frame, "Press SPACE to take selfie", (10, 30))
                self.add_overlay_text(frame, "Press ESC to exit", (10, 70))
            else:
                # Show countdown
                elapsed_time = datetime.datetime.now() - countdown_start
                remaining = countdown_duration - int(elapsed_time.total_seconds())
                
                if remaining > 0:
                    self.add_overlay_text(frame, f"Taking photo in {remaining}...", 
                                       (10, 70), 2, (0, 255, 255))
                else:
                    # Take the selfie
                    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                    filename = os.path.join(self.output_dir, f"selfie_{timestamp}.jpg")
                    cv2.imwrite(filename, frame)
                    print(f"Selfie saved as {filename}")
                    countdown_active = False
            
            # Show the frame
            cv2.imshow('Selfie Camera', frame)
            
            # Handle key presses
            key = cv2.waitKey(1) & 0xFF
            if key == 27:  # ESC key
                break
            elif key == 32 and not countdown_active:  # SPACE key
                countdown_active = True
                countdown_start = datetime.datetime.now()
    
    def release(self):
        """Release the camera and close windows"""
        if self.camera is not None:
            self.camera.release()
        cv2.destroyAllWindows()

def main():
    selfie_cam = WebcamSelfie()
    try:
        selfie_cam.capture_selfie()
    finally:
        selfie_cam.release()

if __name__ == "__main__":
    main()