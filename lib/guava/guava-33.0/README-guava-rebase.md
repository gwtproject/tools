This is version 33.0.0-jre of guava-libraries (Google core Java libraries,
https://github.com/google/guava/).

In order to prevent conflicts with user code which relies on Guava,
we've used jarjar tool provided in this repo to rebase this library.
The "com.google.common" package has been renamed to
"com.google.gwt.thirdparty.guava.common".

To build guava-33.0.0-jre-rebased.jar:

1) Download guava-33.0.0-jre.jar to guava-33.0.0-jre.jar

2a) Use the jarjar tool located at `libs/jarjar-march-01-2024

2b) Rebase guava-33.0.0-jre.jar:
    <jarjar command> process guava-33.0.0-jre.jarjar-rules guava-33.0.0-jre.jar guava-33.0.0-jre-rebased.jar

3) Clean up the resulting jar to remove META-INF:
    zip guava-33.0.0-jre-rebased.jar -d META-INF/*
