# Southbanks Devel

Some scripts I used to generate the overlay regions for the southbank project.

## Notes

1. I copied the original images in the `images_raw` folder.
1. I used GIMP to cut each of the images and save to `.png` files in the `images_raw` folder.
1. `d010_resize_images.py` resizes all cut images and saves them to folder `southbank/images`
1. `d020_capture_rectangles_for_overlay.py` to capture all the outer rectangular regions with the labels. Saved in the `regions/regions.json` file.
1. `d030_scale_regions_as_rectangles.py` generates the scaled regions in the `southbank/overlays.json` file. 
   Here "polygon" is set by default to cover the entire rectangles.
   This step can be skipped. Use `d050_scale_regions_as_polygons.py` instead.
1. I use `d040_capture_regions_for_overlay.py`
1. `d040_capture_regions_for_overlay.py`: used to capture the polygons for the overlays.
1. `d045_capture_check_locations.py`: used to capture the exact point where the check symbols should be shown over each image.
1. `d050_scale_regions_as_polygons.py` computes all the scaling and saves the information for the overlaid polygons in the `southbank/overlays.json` file.

`e010_server.py` serves the web site for local development.
