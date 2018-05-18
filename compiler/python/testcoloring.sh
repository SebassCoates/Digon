python3 digon.py tests/code/valid_stats.di
cp *.txt ../../../graphviewer
cd ../../../graphviewer
python3 graphviewer.py ccfg.txt ccfg_labels.txt --colors=ccfg_colors.txt --root=0
cd ../digon/compiler/python
