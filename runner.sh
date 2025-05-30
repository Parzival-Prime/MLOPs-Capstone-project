echo "Running pipeline..."
dvc repro --force

git add .

echo "Pushing results..."
dvc push

git commit -m "Model retrained!"

echo "Pushing to github..."
git push
echo "All done"