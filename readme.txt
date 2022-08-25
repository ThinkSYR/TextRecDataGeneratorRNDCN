# test for debug
cd trdg
python -u run.py -c 2000 -l ko --space_width 2 --margins -1 --random -w 10 --thread_count 2 -k 8 --random_skew -bl 1.0 --random_blur --background -1 --distorsion -1 --distorsion_orientation -1  -tc "#000000,#666666" --name_format 2 --format 48 --image_dir bgimg/ --output_dir ../test_trdg_debug --label_name "test.txt"