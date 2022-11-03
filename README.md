# SynCheck

## Local run

1. Setup enviroment variables:
 - `TMPIPE_API` - link to the API service that performs text parsing. Code available at https://github.com/OlgaGKononova/TextMiningPipeline
 - `MATBERT_API` - link to the API service that performs text classification. Code available at https://github.com/OlgaGKononova/MatBERT_NER

## Deploying on NERCS:

1. Setup environemnt and make sure you can run `python app.py` without any error.
If you are using landau.lbl.gov desktop, you can use conda environment 
   `source /home/olga/anaconda3/bin/activate syncheck_env` and run from there.
   
2. Make sure you have access to `m1268` project on NERSC and have set up access to their docker repo.

3. Run:
```buildoutcfg
docker build --tag syncheck-app .
docker tag syncheck-app:latest harbor.nersc.gov/m1268/syncheck-app:latest
docker push harbor.nersc.gov/m1268/syncheck-app:latest
```

4. Go to `https://rancher2.spin.nersc.gov/`, m1268 Production, find workload `syncheck-app` and make `redeploy`. 
   
5. Make sure the website `www.syncheck.org` runs correctly. It may take some time for changes to get applied. Usually TMPipe and MatBERT APIs take long time to load.


