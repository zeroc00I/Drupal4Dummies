### How to detect running version:

1. Do a http request and then transform data page result to md5sum. You can do it running this command on bash:

```
curl -sf 'https://example.com/core/misc/drupal.js' | md5sum
```

2. Then, compare the result with the following hashs bellow:

> https://github.com/SamJoan/droopescan/blob/master/dscan/plugins/drupal/versions.xml
