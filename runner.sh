dvc repro --force

git add .

dvc push

git commit -m "Model retrained!"

git push