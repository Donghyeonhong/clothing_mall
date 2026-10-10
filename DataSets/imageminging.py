import pandas as pd
import csv

# 1. styles.csv를 안전하게 읽기
with open("DataSets/styles.csv", "r", encoding="utf-8-sig", newline="") as f:
    reader = csv.reader(f)

    columns = next(reader)
    rows = []

    for row in reader:
        # 열 개수가 원래보다 많으면 마지막 열에 합치기
        if len(row) > len(columns):
            row = row[:len(columns) - 1] + [
                ",".join(row[len(columns) - 1:])
            ]

        # 열 개수가 부족하면 오류 확인
        elif len(row) < len(columns):
            raise ValueError(
                f"열 개수가 부족한 데이터: {row}"
            )

        rows.append(row)

style = pd.DataFrame(rows, columns=columns)


# 2. Apparel 상품만 추출
apparel = style[style["masterCategory"] == "Apparel"]

# 3. Apparel 상품 ID 추출
apparel_ids = apparel["id"].astype(int)

# 4. 이미지 CSV 읽기
image = pd.read_csv("DataSets/images.csv")

# 5. 이미지 파일명에서 상품 ID 추출
image_ids = (
    image["filename"]
    .str.replace(".jpg", "", regex=False)
    .astype(int)
)

# 6. Apparel 상품에 해당하는 이미지만 추출
image_TF = image_ids.isin(apparel_ids)
image_url = image[image_TF]

# 7. 결과 저장
image_url.to_csv("DataSets/cloth_image.csv", index=False)

print("Apparel 상품 수:", len(apparel))
print("추출한 이미지 수:", len(image_url))
print("이미지 CSV 저장 완료!")