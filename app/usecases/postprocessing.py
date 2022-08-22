from __future__ import annotations

from typing import Callable

import blend_modes
import numpy as np
from PIL import Image
from PIL import ImageDraw
from PIL import ImageEnhance
from PIL import ImageFilter
from PIL import ImageOps


def _ensure_image(image: str | Image.Image) -> Image.Image:
    """Ensure image is Image.Image."""

    if isinstance(image, str):
        im = Image.open(image).convert("RGBA")
    else:
        im = image

    return im


def _create_offset_mask(
    image_dim: tuple[int, int],
    offsets: tuple[int, int, int, int],
) -> Image.Image:
    """Create offset mask to keep offseted area safe."""

    mask = Image.new("L", image_dim, 0)
    draw = ImageDraw.Draw(mask)

    draw.rectangle(offsets, fill=255)
    return mask


def _apply_blend_mode(
    image: str | Image.Image,
    colour: tuple[int, int, int],
    opacity: float,
    blend_mode: Callable,
) -> Image.Image:
    """Apply blend function to image."""

    im = _ensure_image(image)
    blend_layer = Image.new("RGBA", im.size, colour)

    layer_float = np.array(im).astype(float)
    blend_layer_float = np.array(blend_layer).astype(float)

    blended_float = blend_mode(layer_float, blend_layer_float, opacity)

    blend_img = Image.fromarray(np.uint8(blended_float))
    return blend_img


def resize_image(image_path: str, dimensions: tuple[int, int]) -> Image.Image:
    """Resize image to given dimetions leaving the same ratio."""

    im = Image.open(image_path).convert("RGBA")
    resized = ImageOps.fit(im, dimensions)

    return resized


def apply_shading(
    image: str | Image.Image,
    colour: tuple[int, int, int],
    opacity: float,
) -> Image.Image:
    """Apply shading effect on layer."""
    return _apply_blend_mode(image, colour, opacity, blend_modes.multiply)


def apply_saturation(
    image: str | Image.Image,
    colour: tuple[int, int, int],
    opacity: float,
) -> Image.Image:
    """Apply saturation effect on layer."""
    return _apply_blend_mode(image, colour, opacity, blend_modes.hard_light)


def apply_new_brightness(
    image: str | Image.Image,
    offsets: tuple[int, int, int, int],
    opacity: float,
) -> Image.Image:
    """Apply new brightness value to image."""

    im = _ensure_image(image)
    mask = _create_offset_mask(im.size, offsets)
    brightness = ImageEnhance.Brightness(im).enhance(opacity)

    brightness.paste(im, mask=mask)
    return brightness


def apply_gaussian_blur(
    image: str | Image.Image,
    offsets: tuple[int, int, int, int],
    blur_radius: int,
) -> Image.Image:
    """Apply gaussian filter to image."""

    im = _ensure_image(image)
    mask = _create_offset_mask(im.size, offsets)
    blurred = im.filter(ImageFilter.GaussianBlur(blur_radius))

    blurred.paste(im, mask=mask)
    return blurred


def apply_effects_normal_template(image_path: str) -> Image.Image:
    """Apply effects for normal score template."""

    im = resize_image(image_path, (1920, 1080))
    im1 = apply_new_brightness(im, (0, 0, 1920, 244), 0.63)
    im2 = apply_gaussian_blur(im1, (0, 0, 1920, 244), 3)
    im3 = apply_shading(im2, (0, 0, 0), 0.39)
    im4 = apply_saturation(im3, (13, 13, 97), 0.20)

    return im4


def apply_effects_knockout_template(image_path: str) -> Image.Image:
    """Apply effects for knockout template."""

    im = resize_image(image_path, (1920, 1080))
    im1 = apply_shading(im, (0, 0, 0), 0.10)
    im2 = apply_gaussian_blur(im1, (0, 0, 1920, 0), 3)
    im3 = apply_saturation(im2, (13, 13, 97), 0.10)

    return im3
