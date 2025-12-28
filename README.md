# Crack Detector

建物やインフラのクラック（ひび割れ）を検出・マッピングするためのツール群です。

## 機能

### デスクトップアプリ（Python/OpenCV）

画像ファイルからクラックを検出し、視覚化します。

- **クラック検出**: Canny、Sobel、Laplacianによるエッジ検出
- **透視変換**: 4点指定による画像の射影変換
- **グリッド表示**: 検査エリアをグリッド分割して表示
- **コントラスト強調**: CLAHE（適応的ヒストグラム平坦化）によるクラックの視認性向上
- **クラック面積計算**: 検出されたクラックの面積率を自動計算

### Webアプリ

スマートフォンのカメラを使用してクラック展開図を作成します。

- **カメラ撮影**: フロント/リアカメラの切り替え対応
- **グリッドマッピング**: 3x3、4x4、5x5のグリッドで撮影位置を管理
- **リアルタイムクラック検出**: Sobelフィルタによるエッジ検出
- **統計表示**: 平均/最大クラック率、総クラック面積の表示

## 必要要件

### デスクトップアプリ

- Python 3.x
- OpenCV (`cv2`)
- NumPy
- Pillow

```bash
pip install opencv-python numpy pillow
```

### Webアプリ

- モダンブラウザ（Chrome、Safari、Firefox等）
- カメラへのアクセス許可

## 使い方

### デスクトップアプリ

```python
from crack_detector import detect_cracks
import cv2

# 画像を読み込み
image = cv2.imread('your_image.jpg')

# クラック検出を実行
result = detect_cracks(image, method='canny', threshold1=25, threshold2=50, clip_limit=5.0)

# 結果を表示
cv2.imshow('Crack Detection', result)
cv2.waitKey(0)
```

### Webアプリ

1. `webapp/index.html` または `docs/index.html` をブラウザで開く
2. カメラへのアクセスを許可
3. 展開図のセルをタップして撮影位置を選択
4. 撮影ボタンで撮影
5. プレビューを確認して保存

GitHub Pages: `docs/index.html` を使用してデプロイ可能

## プロジェクト構成

```
crack_detector/
├── crack_detector.py      # クラック検出ロジック
├── transform_controller.py # 透視変換制御
├── grid_controller.py     # グリッド表示・制御
├── settings_window.py     # 設定ウィンドウ
├── undistort.py          # レンズ歪み補正
├── transformer/          # 変換処理モジュール
│   ├── perspective_transform.py
│   └── vertical_transform.py
├── draw_grid/            # グリッド描画モジュール
│   └── draw_grid.py
├── utils/                # ユーティリティ
│   ├── copy_image_to_clipboard.py
│   └── select_file.py
├── webapp/               # Webアプリ
│   └── index.html
└── docs/                 # GitHub Pages用
    └── index.html
```

## ライセンス

MIT License
