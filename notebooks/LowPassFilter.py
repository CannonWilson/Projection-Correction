from collections import deque
import numpy as np
from PIL import Image

# notes: I think this can be made more performant by implementing a threaded timer to update the buffer, but that
# would be a lot of work to make sure it plays nice with the rest of the code. If the overhead is too high, we can
# consider this as an optimization later.

class LowPassFilter:
    """
    A low pass filter to smooth out the pixel-wise deltas between frames, reducing flicker. Uses
    a cyclic buffer to store the prior N deltas and calculate the average delta to apply to the measured frame.
    The frame is then clipped and returned as a corrected frame.

    Instantiate it and then feed the beast the frames it craves. (Using the apply filter method)
    """
    def __init__(self, buffer_size: int = 5):
        """
        Initializes the low pass filter with a specified buffer size (default length of 5).

        :param buffer_size: Integer to define the size of the cycle buffer.
        """

        # the max buffer size
        #  -> larger means higher overhead but more stable
        #  -> smaller means lower overhead but less stable
        self.buffer_size = buffer_size
        self.deltas_buffer = deque(maxlen=buffer_size) # use deque as cyclic buffer
        self.current_true_frame = None  # placeholder for the current true frame as a NumPy array
        self.current_measured_frame = None # placeholder for the current measured frame as a NumPy array

    def _compute_delta(self) -> np.ndarray:
        """
        Computes the pixel-wise delta between the true frame and the measured frame
        for all color channels. This method is intended for internal use.

        :return: NumPy array of pixel-wise deltas.
        """
        return self.current_true_frame - self.current_measured_frame # calculate the pixel-wise delta

    def _update_buffer(self, delta: np.ndarray):
        """
        Updates the cycle buffer with the new delta, maintaining the buffer size.
        This method is intended for internal use.

        :param delta: NumPy array of pixel-wise deltas to add to the buffer.
        """
        self.deltas_buffer.append(delta) # uses deque as cyclic buffer -> overwrites oldest member when full

    def _calculate_average_delta(self) -> np.ndarray:
        """
        Calculates the average delta from the deltas present in the buffer.
        This method is intended for internal use.

        :return: NumPy array representing the average pixel-wise delta.
        """
        if not self.deltas_buffer:
            return np.array([]) # return empty array if buffer is empty

        return np.mean(np.stack(self.deltas_buffer), axis=0) # calculate and return mean of all deltas in buffer

    def apply_filter(self, true_frame: Image.Image, measured_frame: Image.Image) -> Image.Image:
        """
        Main method to accept frames, compute delta, update buffer,
        calculates the average delta, applies the delta to the measured frame,
        and returns the corrected frame.

        :param true_frame: PIL Image representing the true frame.
        :param measured_frame: PIL Image representing the measured frame.
        :return: PIL Image representing the corrected frame.
        """
        # Example conversion from PIL Image to NumPy array
        self.current_true_frame = np.array(true_frame)
        self.current_measured_frame = np.array(measured_frame)

        # Compute pixel-wise delta
        delta = self._compute_delta()

        # Update the buffer with the new delta
        self._update_buffer(delta)

        # Calculate the average delta
        avg_delta = self._calculate_average_delta()

        # Apply the average delta to the true frame (push the measured frame towards the true frame)
        corrected_frame = self.current_true_frame + avg_delta

        # clip the values to be between 0 and 255
        corrected_frame = np.clip(corrected_frame, 0, 255).astype(np.uint8)

        # Convert NumPy array to PIL Image
        return Image.fromarray(corrected_frame)
