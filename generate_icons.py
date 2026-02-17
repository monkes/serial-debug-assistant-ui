#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
图标生成脚本 - 用于生成简单的占位图标
"""

from PIL import Image, ImageDraw, ImageFont
import os

def create_icon(size, output_path):
    """创建指定尺寸的图标"""
    # 创建图像
    img = Image.new('RGBA', (size, size), (70, 130, 180, 255))
    draw = ImageDraw.Draw(img)

    # 绘制边框
    border_width = max(2, size // 20)
    draw.rectangle(
        [(border_width, border_width), (size - border_width - 1, size - border_width - 1)],
        outline=(255, 255, 255, 255),
        width=border_width
    )

    # 绘制"DA"文字（Debug Assistant的缩写）
    try:
        font_size = size // 2
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", font_size)
    except:
        font = ImageFont.load_default()

    text = "DA"
    text_width, text_height = draw.textsize(text, font=font) if hasattr(draw, 'textsize') else (size//2, size//2)
    position = ((size - text_width) // 2, (size - text_height) // 2)
    draw.text(position, text, fill=(255, 255, 255, 255), font=font)

    # 保存图像
    img.save(output_path)
    print(f"已创建图标: {output_path}")

def main():
    """主函数"""
    # 确保resources目录存在
    resources_dir = os.path.join(os.path.dirname(__file__), "debug_assistant", "resources")
    if not os.path.exists(resources_dir):
        os.makedirs(resources_dir)

    # 创建不同尺寸的图标
    sizes = [256, 128, 64, 48]
    for size in sizes:
        output_path = os.path.join(resources_dir, f"icon{size}x{size}.png")
        create_icon(size, output_path)

    print("\n所有图标已生成完成！")

if __name__ == "__main__":
    main()
