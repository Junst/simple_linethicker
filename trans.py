from PIL import Image
import cairosvg
import subprocess
import io
import os

def pil_image_to_svg_to_pil_image(pil_image):
    try:
        # 투명 배경을 흰색으로 변환
        if pil_image.mode == 'RGBA':
            background = Image.new('RGBA', pil_image.size, (255, 255, 255))
            pil_image = Image.alpha_composite(background, pil_image).convert('RGB')
        
        # PIL 이미지를 BMP 바이너리 데이터로 변환
        bmp_io = io.BytesIO()
        pil_image.save(bmp_io, format='BMP')
        bmp_data = bmp_io.getvalue()
        
        # potrace를 사용하여 BMP를 SVG로 변환
        bmp_file_path = '/tmp/temp.bmp'
        svg_file_path = '/tmp/temp_svg.svg'
        
        with open(bmp_file_path, 'wb') as bmp_file:
            bmp_file.write(bmp_data)
        
        command = f'potrace "{bmp_file_path}" -s -o "{svg_file_path}"'
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        
        if result.returncode != 0:
            raise RuntimeError(f"Error occurred during potrace execution: {result.stderr}")
        
        # BMP 파일 삭제
        os.remove(bmp_file_path)
        
        with open(svg_file_path, 'rb') as svg_file:
            svg_data = svg_file.read()
        
        # SVG 데이터를 PNG로 변환하여 PIL 이미지로 읽기
        png_data = cairosvg.svg2png(bytestring=svg_data, background_color=None)
        output_image = Image.open(io.BytesIO(png_data))
        
        # SVG 파일 삭제
        os.remove(svg_file_path)
        
        return output_image
    
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return None


if __name__ == '__main__':
    # 테스트 코드
    input_image = Image.open('')
    output_image = pil_image_to_svg_to_pil_image(input_image)
    output_image.save('output.png')