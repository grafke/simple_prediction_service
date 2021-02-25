# Project Skyhawk

    
### Getting Started:
To begin with, you'll have to deploy the service. You can do it by running the following commands:  
    
    ./bin/build.sh  
    ./bin/run_docker.sh  
    
After that, open your browser, go to http://localhost:8000/, and upload an .mp4 file.
After a video has been uploaded and processed, you should see the following response:  
    ```
    {  
      "p_real": 0,  
      "p_fake": 0  
    }  
    ```

Auto-generated documentation is available here: http://localhost:8000/docs

Note: you can also run the service without docker:  

     ./bin/start.sh
    

    
