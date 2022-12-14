#!/usr/bin/bash

declare -A chrome_versions

# From https://github.com/aws-samples/serverless-ui-testing-using-selenium
# Enter the list of browsers to be downloaded
### Using Chromium as documented here - https://www.chromium.org/getting-involved/download-chromium
chrome_versions=( ['109.0.5414.25']='1070081' )
#['89.0.4389.47']='843831' ) #['88.0.4324.150']='827102'
chrome_drivers=( "109.0.5414.25" )
#"89.0.4389.23" ) #"88.0.4324.96"
firefox_versions=( "87.0b3" ) #"86.0" 
gecko_drivers=( "0.29.0" )

# Download Chrome
for br in "${!chrome_versions[@]}"
do
    echo "Downloading Chrome version $br"
    mkdir -p "/opt/chrome/$br"
    curl -Lo "/opt/chrome/$br/chrome-linux.zip" "https://www.googleapis.com/download/storage/v1/b/chromium-browser-snapshots/o/Linux_x64%2F${chrome_versions[$br]}%2Fchrome-linux.zip?alt=media"
    unzip -q "/opt/chrome/$br/chrome-linux.zip" -d "/opt/chrome/$br/"
    mv /opt/chrome/$br/chrome-linux/* /opt/chrome/
    ln -s /opt/chrome/chrome /opt/chrome/google-chrome
    rm -rf /opt/chrome/$br/chrome-linux "/opt/chrome/$br/chrome-linux.zip"
done

# Download Chromedriver
for dr in ${chrome_drivers[@]}
do
    echo "Downloading Chromedriver version $dr"
    mkdir -p "/opt/chromedriver/$dr"
    curl -Lo "/opt/chromedriver/$dr/chromedriver_linux64.zip" "https://chromedriver.storage.googleapis.com/$dr/chromedriver_linux64.zip"
    unzip -q "/opt/chromedriver/$dr/chromedriver_linux64.zip" -d "/opt/chromedriver/"
    chmod +x "/opt/chromedriver/chromedriver"
    rm -rf "/opt/chromedriver/$dr/chromedriver_linux64.zip"
done

: << 'COMMENT'
No current need for firefox support, keeping the container as light as possible

# Download Firefox
for br in ${firefox_versions[@]}
do
    echo "Downloading Firefox version $br"
    mkdir -p "/opt/firefox/$br"
    curl -Lo "/opt/firefox/$br/firefox-$br.tar.bz2" "http://ftp.mozilla.org/pub/firefox/releases/$br/linux-x86_64/en-US/firefox-$br.tar.bz2"
    tar -jxf "/opt/firefox/$br/firefox-$br.tar.bz2" -C "/opt/firefox/$br/"
    mv "/opt/firefox/$br/firefox" "/opt/firefox/$br/firefox-temp"
    mv /opt/firefox/$br/firefox-temp/* /opt/firefox/$br/
    rm -rf "/opt/firefox/$br/firefox-$br.tar.bz2"
done

# Download Geckodriver
for dr in ${gecko_drivers[@]}
do
    echo "Downloading Geckodriver version $dr"
    mkdir -p "/opt/geckodriver/$dr"
    curl -Lo "/opt/geckodriver/$dr/geckodriver-v$dr-linux64.tar.gz" "https://github.com/mozilla/geckodriver/releases/download/v$dr/geckodriver-v$dr-linux64.tar.gz"
    tar -zxf "/opt/geckodriver/$dr/geckodriver-v$dr-linux64.tar.gz" -C "/opt/geckodriver/$dr/"
    chmod +x "/opt/geckodriver/$dr/geckodriver"
    rm -rf "/opt/geckodriver/$dr/geckodriver-v$dr-linux64.tar.gz"
done
COMMENT