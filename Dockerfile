FROM  --platform=linux/amd64 openjdk:17-slim
# ENV AVD_NAME android33
ARG AVD_NAME
ENV AVD_NAME ${AVD_NAME}
ENV ANDROID_SDK_TOOLS 9477386
ENV ANDROID_SDK_URL https://dl.google.com/android/repository/commandlinetools-linux-${ANDROID_SDK_TOOLS}_latest.zip
ENV ANDROID_BUILD_TOOLS_VERSION 33.0.0
ENV ANDROID_HOME /root/android/sdk
ENV ANDROID_VERSION 33
ENV QT_DEBUG_PLUGINS=1
ENV PATH $PATH:$ANDROID_HOME/tools:$ANDROID_HOME/tools/bin:$PATH:$ANDROID_HOME/platform-tools:$ANDROID_HOME/cmdline-tools/bin:$ANDROID_HOME/emulator

# Set user to root for necessary permissions
USER root


# Install required packages
RUN apt-get update && \
    apt-get install -y vim libqt5gui5 procps libxcb-cursor0 pulseaudio libnss3-dev libgdk-pixbuf2.0-dev libgtk-3-dev libxss-dev && \
    apt-get install -y --no-install-recommends unzip curl && \
    mkdir -p "$ANDROID_HOME" .android && \
    cd "$ANDROID_HOME" && \
    curl -o sdk.zip $ANDROID_SDK_URL && \
    unzip sdk.zip && \
    rm sdk.zip && \
# Download Android SDK
    yes | sdkmanager --licenses --sdk_root=$ANDROID_HOME && \
    sdkmanager --update --sdk_root=$ANDROID_HOME && \
    sdkmanager --sdk_root=$ANDROID_HOME "build-tools;${ANDROID_BUILD_TOOLS_VERSION}" \
    "platforms;android-${ANDROID_VERSION}" \
    "platform-tools" \
    "emulator" \
    "extras;android;m2repository" \
    "extras;google;m2repository" && \
# Clean up
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/* && \
    apt-get autoremove -y && \
    apt-get clean




RUN sdkmanager --sdk_root=$ANDROID_HOME --install "system-images;android-33;google_apis_playstore;x86_64"


# RUN echo "ANDROID_SDK_ROOT=${ANDROID_HOME}" >> ~/.bashrc
# RUN echo "ANDROID_HOME=${ANDROID_HOME}" >> ~/.bashrc

RUN echo "no" | avdmanager  create avd  --name $AVD_NAME --package "system-images;android-33;google_apis_playstore;x86_64" 

RUN sed -i -e 's/sysdir.1=sdk\//sysdir.1=/g' /root/.android/avd/$AVD_NAME.avd/config.ini




RUN echo "Ubuntu base container is Build!"


# -no-window Parameters must to add!
# RUN emulator -avd $AVD_NAME -gpu swiftshader_indirect -no-audio -no-boot-anim 

# docker run -it --rm -e "DISPLAY=$DISPLAY"  -v "$HOME/.Xauthority:/root/.Xauthority:ro"  \
#  --network host --name a-container --device /dev/kvm  b /bin/bash


# Replace shell with bash so we can source files
# RUN rm /bin/sh && ln -s /bin/bash /bin/sh

# Set debconf to run non-interactively
# RUN echo 'debconf debconf/frontend select Noninteractive' | debconf-set-selections


# ENV NVM_DIR /root/.nvm
# ENV NODE_VERSION 16.13.0

# # Install nvm with node and npm
# RUN curl -sL https://raw.githubusercontent.com/creationix/nvm/v0.35.3/install.sh | bash \
#   && . $NVM_DIR/nvm.sh \ 
#   && nvm install $NODE_VERSION


# replace shell with bash so we can source files
RUN rm /bin/sh && ln -s /bin/bash /bin/sh

# nvm environment variables
ENV NVM_DIR /root/nvm
ENV NODE_VERSION 16.13.0

RUN mkdir -p $NVM_DIR

# install nvm
# https://github.com/creationix/nvm#install-script
RUN curl --silent -o- https://raw.githubusercontent.com/creationix/nvm/v0.35.3/install.sh | bash

ENV NODE_PATH $NVM_DIR/v$NODE_VERSION/lib/node_modules
ENV PATH $NVM_DIR/versions/node/v$NODE_VERSION/bin:$PATH

RUN echo "source $NVM_DIR/nvm.sh && \
    nvm install $NODE_VERSION && \
    nvm alias default $NODE_VERSION && \
    nvm use default" | bash

# confirm installation
RUN node -v
RUN npm -v



# appium 2.0.1
# RUN npm i -g appium

# RUN appium driver install uiautomator2
# RUN npm i -g appium-doctor


