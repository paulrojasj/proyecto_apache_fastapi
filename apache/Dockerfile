FROM httpd:2.4

RUN sed -i 's/#LoadModule proxy_module/LoadModule proxy_module/' /usr/local/apache2/conf/httpd.conf && \
    sed -i 's/#LoadModule proxy_http_module/LoadModule proxy_http_module/' /usr/local/apache2/conf/httpd.conf

COPY fastapi.conf /usr/local/apache2/conf/extra/httpd-vhosts.conf

RUN sed -i 's|#Include conf/extra/httpd-vhosts.conf|Include conf/extra/httpd-vhosts.conf|' /usr/local/apache2/conf/httpd.conf
