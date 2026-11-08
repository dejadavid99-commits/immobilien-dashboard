from PIL import Image, ImageDraw

SIZE = 1024  # supersampled, then downscaled for crisp edges
GREEN = (31, 157, 85, 255)   # matches --accent
WHITE = (255, 255, 255, 255)

img = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
draw = ImageDraw.Draw(img)

# Rounded-square background
radius = int(SIZE * 0.22)
draw.rounded_rectangle([0, 0, SIZE - 1, SIZE - 1], radius=radius, fill=GREEN)

# House silhouette (roof + body), centered-low
cx = SIZE * 0.42
body_left, body_right = SIZE * 0.24, SIZE * 0.60
body_top, body_bottom = SIZE * 0.50, SIZE * 0.74
roof_tip_y = SIZE * 0.30
eave = SIZE * 0.05

draw.polygon(
    [(body_left - eave, body_top), (cx, roof_tip_y), (body_right + eave, body_top)],
    fill=WHITE,
)
draw.rectangle([body_left, body_top, body_right, body_bottom], fill=WHITE)

# Door cutout (green, to show background through the house)
door_w, door_h = SIZE * 0.08, SIZE * 0.14
door_cx = cx
draw.rectangle(
    [door_cx - door_w / 2, body_bottom - door_h, door_cx + door_w / 2, body_bottom],
    fill=GREEN,
)

# Upward growth arrow (white), rising from lower-left to upper-right past the roof
line_w = int(SIZE * 0.045)
p1 = (SIZE * 0.40, SIZE * 0.70)
p2 = (SIZE * 0.56, SIZE * 0.52)
p3 = (SIZE * 0.68, SIZE * 0.58)
p4 = (SIZE * 0.84, SIZE * 0.26)
draw.line([p1, p2, p3, p4], fill=WHITE, width=line_w, joint="curve")
for p in (p2, p3):
    r = line_w * 0.55
    draw.ellipse([p[0]-r, p[1]-r, p[0]+r, p[1]+r], fill=WHITE)

# Arrowhead at the end of the trend line
ax, ay = p4
head_len = SIZE * 0.10
head_w = SIZE * 0.07
draw.polygon(
    [
        (ax, ay),
        (ax - head_len, ay + head_w * 0.25),
        (ax - head_len * 0.45, ay + head_w),
    ],
    fill=WHITE,
)

sizes = {
    "icon-512.png": 512,
    "icon-192.png": 192,
    "apple-touch-icon.png": 180,
    "favicon-32.png": 32,
    "favicon-16.png": 16,
}
for name, s in sizes.items():
    img.resize((s, s), Image.LANCZOS).save(name)

print("Icons geschrieben:", ", ".join(sizes))
