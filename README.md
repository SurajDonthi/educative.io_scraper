# Educative.io Scraper -- Educative.io Downloader

<pre><code style="white-space : pre-wrap !important;">Description: 
This tool effortlessly scrapes and saves Educative.io courses for offline use enabling you to
learn at your own pace, even without an internet connection.

Contributions:
I wholeheartedly welcome contributions from individuals in any capacity to enhance this project.
Thank you for your support!

Disclaimer:
I want to clarify that I am not accountable for any inappropriate use of this scraper. 
I developed it solely for research purposes and take no responsibility for its misuse.

Repository Version: v3.8.0 (Recommended)
Master Branch: v3-master</code></pre>
```
1. Updates Information
-  SandPack code container support added
-  SingleFile injection script now uses single-file-cli logic instead of custom (v3.7.4) 
-  Injectes SingleFile through Local. Script faster by 10 seconds per topic, fixes Iframe (v3.7.3)
-  AutoFixUrl and AutoResume were added (v3.6.5+)
      * AutoFixUrl: The urls text file will be automatically updated based on the last topic URL from the Log File.
        If a manual edit was done on the text file then consider unchecking this option.
      * AutoResume (Recommended): Retries 3/4 times if there is any error occurs for a specific URL.
        If it still fails, then consider checking the log for more details. 
-  Undetected driver replaced by SeleniumBase (Bypass Cloudflare Turnstile) (v3.5.7+)
-  Run with --install arg again OR manually clean install (v3.5.7+)
-  Delete the old UserDataDir (v3.5.5+)
-  No existing Chrome browser should be running in the background (v3.4.2+)     
-  Redownload Chrome Binary and Chrome driver. (v3.4.2+)
-  If Undetected/SeleniumBase does not work then UNCHECK and use default webdriver. (v3.4.2+)
2. Send a mail notification status, Setup here: /src/Main/MailNotify.py
```
###                                

## To view the downloaded courses, you can use the [Educative-Viewer](https://github.com/anilabhadatta/educative-viewer) repository, which provides a better readability and user-friendly interface for accessing the downloaded course content.

## Steps to use the scraper:

-  ### Prerequisites:

```
Git
Python 3.12 or more
OS: Win(x86/x64) - Mac(ARM64/x64) - Linux(ARM64/x64)
```

-  ### Download & cd this project dir.

```
git clone https://github.com/anilabhadatta/educative.io_scraper.git
cd educative.io_scraper
   ```

-  ### Run the following commands to start Educative Scraper.
- #### Automatic Steps:
    - #### Use python3 instead of python for Linux and MacOS.
      ```
      python setup.py --install
      python setup.py --run
      
      [Commands]
      --install: Creates a virtual environment and installs the required dependencies.
      --run: Activates the environment and starts the scraper. [Default = True]
      --create: Creates a shortcut executable file linked to the scraper directory.
            
            If the git repository is moved to a different location after creating
            the executable then recreate it again to set the new repository path.
      ```


- #### Manual Steps:
    - #### Windows:
      ```
      pip install virtualenv
      python -m venv env <or> virtualenv env
      env\Scripts\activate
      pip install -r requirements.txt
      python EducativeScraper.py
      ```
    - #### MacOS/Linux:
      ```
      pip3 install virtualenv
      python3 -m venv env <or> virtualenv env
      source env/bin/activate
      pip3 install -r requirements.txt
      python3 EducativeScraper.py
      ```
      <div align="center">
         <figure>
            <img src="https://github.com/anilabhadatta/educative.io_scraper/assets/48487849/8d2fc780-dd82-43b5-8c8c-c58b6c2213b9" style="width: 50%; height:50%;">
            <br>
            <figcaption>Recommeded GUI Settings</figcaption>
         </figure>
      </div>


-  ### After the GUI successfully loads, please proceed to follow the subsequent steps.
    - Create a text file.
    - Copy the URLs of the first topic/lesson from any number of courses.
    - Paste all the URLs into the text file and save it.
      <div align="center">
       <br><img src="https://user-images.githubusercontent.com/48487849/162980989-0f128b3d-c969-4809-8553-2bc6791f34b8.png" style="width: 70%; height:50%;">
       <br>
         <figure><img src="https://user-images.githubusercontent.com/48487849/197013915-1320da6b-d2c2-4239-b1f7-d95450f8fabb.png" style="width: 70%; height:50%;"><br>
          <figcaption>Reference</figcaption>
         </figure>
      </div>

    - Select a configuration if you prefer not to use the default configuration.
    - If you prefer not to display the browser window, choose the `headless` option.
    - Please provide a unique `User Data Directory` name that the browser will use to store your current session. Ensure
      that `each instance` of the scraper has a `distinct` User Data Directory name.
    - Please select the file path of the text file containing the course URLs, as well as the directory where you would
      like to save the downloaded content.
    - You can choose to save/export the current configuration for later use, or you can opt for the default
      configuration.
    - For the initial setup or updates, click on `Download Chromedriver` and `Download Chrome Binary` to automatically
      Download them into the project directory.
    - If you intend to utilize proxies, simply enable the proxy option and enter the proxy in proxies box.
      <ul>
      <br>
        <li> For IP authorized proxy, you can directly enter IP:PORT of the proxy.</li>
        <li> For USER:PASS authorized proxy, you'll need to create a localhost tunnel using the <a href="https://github.com/anilabhadatta/proxy-login-automator">Proxy-Login-Automator</a> repository.</li>
        <li> After setting up the tunnel, enter the IP:PORT of the localhost proxy that you configured in the Proxy Login Automator.</li>
        <br>
      </ul>
    - Click on `Login Account` to log in to your Educative.io account and click on `Close Browser Button` to close the
      browser after the login is completed.
    - Click on `Start Scraper` to begin scraping the courses.
    - The scraper will automatically stop after scraping all the URLs in the selected text file.
    - If you decide to stop the scraper using the `Stop Scraper Button` before it finishes or face any errors, the most
      recent URL will be saved in the `EducativeScraper.log` file. Simply copy the URL from the INFO logger and replace
      the URL of the topic/lesson that has already been completed with the copied URL. This will allow you to resume the
      scraper from where you left off.
      <div align="center">
      <br><img src="https://github-production-user-asset-6210df.s3.amazonaws.com/48487849/264581350-dd669e5a-739c-4ff1-a7b3-6beb2eba5437.png" style="width: 80%; height:80%;">
      </div>
    - An index is `NOT` required in the URL's text file, Simply paste the URLs of the topic from which you
      want to start/resume scraping.
