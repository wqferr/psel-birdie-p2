cd ../classification
python classify.py 0.2
cp labeled_data.tsv ../feature_extraction/
cd ../feature_extraction
python filter_smartphones.py labeled_data.tsv smartphones.tsv
