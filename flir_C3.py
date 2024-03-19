import cv2
import matplotlib.pyplot as plt
import os
import numpy as np
import os.path
from matplotlib import pyplot as plt
from flir_image_extractor import FlirImageExtractor

class FlirC3(FlirImageExtractor):
    def __init__(self, exiftool_path="exiftool", is_debug=False):
        super().__init__(exiftool_path, is_debug)

    def cropped_and_resized(self, scale=0.7, margin_top=-2, margin_left=-16):
        # Ensure the images have been processed
        if self.rgb_image_np is None or self.thermal_image_np is None:
            raise ValueError(
                "Images not processed. Please run process_image() first.")

        # Calculate output dimensions
        output_height = int(480 * scale)
        output_width = int(640 * scale)

        # Resize thermal image
        thermal_resized = cv2.resize(
            self.thermal_image_np, (output_width, output_height), interpolation=cv2.INTER_LINEAR)

        # Calculate borders for cropping RGB image
        border_x = (self.rgb_image_np.shape[0] - output_height) // 2
        border_y = (self.rgb_image_np.shape[1] - output_width) // 2

        # Crop and adjust RGB image with margins
        rgb_cropped = self.rgb_image_np[border_x + margin_left:border_x + margin_left + output_height,
                                        border_y - margin_top:border_y - margin_top + output_width]

        self.rgb_cropped = rgb_cropped
        self.thermal_resized = thermal_resized

    def plot_cropped_and_resized(self):
        # Display both images for comparison
        _, ax = plt.subplots(1, 2, figsize=(10, 5))
        ax[0].imshow(self.thermal_resized, cmap='jet')
        ax[1].imshow(self.rgb_cropped)

    def get_rgb_cropped_np(self):
        return self.rgb_cropped

    def get_thermal_resized_np(self):
        return self.thermal_resized

    def save_images_crop_resize(self, path_save=None):
        # Setup filenames
        if path_save is None:
            fn_prefix, _ = os.path.splitext(self.flir_img_filename)
            save_fileName = fn_prefix + "_hyperspectral.tiff"
        else:
            fileName = os.path.basename(self.flir_img_filename)
            save_fileName = os.path.join(path_save, fileName)
            save_fileName = os.path.splitext(save_fileName)[0] + ".tiff"

        # Ensure the save directory exists
        if not os.path.exists(os.path.dirname(save_fileName)):
            os.makedirs(os.path.dirname(save_fileName))

        # Convert RGB to correct color format if necessary
        rgb_corrected = cv2.cvtColor(self.rgb_cropped, cv2.COLOR_BGR2RGB)

        rgb_int = np.array(rgb_corrected, dtype=np.float16)
        thermal_float = self.thermal_resized.astype(np.float16)
        hyperspectral_image = np.dstack((rgb_int, thermal_float*10))
        cv2.imwrite(save_fileName, hyperspectral_image,
                    [cv2.IMWRITE_TIFF_COMPRESSION, 1])


def main():
    files = [filename for filename in os.listdir(
        ".") if filename.endswith(".jpg")]
    total_files = len(files)
    for index, filename in enumerate(files):
        fir = FlirC3()
        fir.process_image(filename)
        fir.cropped_and_resized()
        fir.save_images_crop_resize("multispectral/")
        remaining_files = total_files - (index + 1)
        print(f"Processed {filename}. Remaining files: {remaining_files}")


if __name__ == "__main__":
    print("Starting...")
    main()
