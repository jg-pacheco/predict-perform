# Loading the Data
Create a fresh environment and install the requirements.txt file
```unix
conda create -n predict-perform python==3.9.12
conda activate predict-perform
```
```
pip install -r requirements.txt
```
Now you should be able to load the data using the following command. **Note: Only do this once as the website will ban you if repeated within an hour**
```python
python load_data.py
```

