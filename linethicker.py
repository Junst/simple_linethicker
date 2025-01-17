import numpy as np
from PIL import Image
import cairosvg

# # 먼저 svg로 변환해줘
# # 그 다음에 svg로 변환된 이미지를 불러와서 두껍게 만들어줘
# def image_to_svg(image_path, svg_path):
#     # 이미지 열기
#     image = Image.open(image_path)
    
#     # 이미지 크기
#     width, height = image.size
    
#     # SVG 파일로 저장
#     cairosvg.svg2svg(url=image_path, write_to=svg_path)

def thicken_line_with_transparency(image, thickness=3):
    """
    이미지의 선을 두껍게 만들되, 투명한 부분은 유지하는 함수.

    Parameters:
        image (PIL.Image): 원본 이미지 (RGBA).
        thickness (int): 선의 두께를 늘릴 정도.

    Returns:
        PIL.Image: 선이 두꺼워진 이미지 (RGBA).
    """
    # RGBA 모드로 변환
    image = image.convert("RGBA")
    rgba_data = np.array(image)
    
    # RGB 데이터와 알파 채널 분리
    rgb_data = rgba_data[:, :, :3]
    alpha_channel = rgba_data[:, :, 3]
    
    # 선(Line) 영역만 추출 (알파 채널이 0이 아니고, RGB 값이 흰색이 아님)
    line_mask = (alpha_channel > 0) & (np.any(rgb_data < 255, axis=-1))  # 선 부분만 True
    
    # NumPy 배열로 팽창
    binary_array = line_mask.astype(np.uint8)
    padded_array = np.pad(binary_array, thickness, mode='constant', constant_values=0)
    
    # 팽창 연산
    for _ in range(thickness):
        shifted_up = np.roll(padded_array, 1, axis=0)  # 위로 이동
        shifted_down = np.roll(padded_array, -1, axis=0)  # 아래로 이동
        shifted_left = np.roll(padded_array, 1, axis=1)  # 왼쪽으로 이동
        shifted_right = np.roll(padded_array, -1, axis=1)  # 오른쪽으로 이동
        
        # 병합
        padded_array = np.maximum.reduce([padded_array, shifted_up, shifted_down, shifted_left, shifted_right])
    
    # 다시 원본 크기로 자르기
    thickened_array = padded_array[thickness:-thickness, thickness:-thickness]
    
    # 새로운 알파 채널 생성 (팽창된 선을 기준으로)
    new_alpha_channel = (thickened_array * 255).astype(np.uint8)
    
    # RGB 데이터는 원래 값을 유지
    new_rgb_data = np.where(thickened_array[:, :, None], rgb_data, 0)  # 팽창된 선 부분만 유지
    
    # RGBA 데이터 병합
    thickened_rgba_data = np.dstack((new_rgb_data, new_alpha_channel))
    thickened_image = Image.fromarray(thickened_rgba_data, mode="RGBA")
    
    return thickened_image




if __name__ == "__main__":
    # 이미지 열기
    image_path = ""
    image = Image.open(image_path)

    ## 이미지를 SVG로 변환
    #svg_path = "sample.svg"
    #image_to_svg(image_path, svg_path)
    
    
    thickness = 5
    # 선 두껍게 만들기
    thickened_image = thicken_line_with_transparency(image, thickness)
    
    # 이미지 저장
    thickened_image.save(f"")
    print("이미지 저장 완료")