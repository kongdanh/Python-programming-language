import random

# Danh sách các loại ô (ví dụ: 9 loại)
tile_types = ['apple', 'banana', 'cherry', 'grape', 'lemon', 'orange', 'peach', 'pear', 'watermelon']

# Tạo danh sách các ô, mỗi loại có 3 ô
tiles = tile_types * 3  # Tổng cộng 27 ô

# Xáo trộn danh sách ô
random.shuffle(tiles)

# Gán vị trí cho từng ô (ví dụ: trong lưới 5x6)
positions = [(x, y) for x in range(5) for y in range(6)]
random.shuffle(positions)

# Kết hợp ô với vị trí
tile_positions = list(zip(tiles, positions))

print(tile_positions)