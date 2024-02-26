This is version 1.0.2 of failureaccess (Google core Java libraries,
https://github.com/google/guava/tree/master/futures/failureaccess).

The link 
[here](https://github.com/google/guava/blob/5f7750959a391e78ae17165921933b78a3a815d5/futures/failureaccess/pom.xml#L14) 
describes why we need 
In order to prevent conflicts with user code which relies on Guava,
we've used jarjar tool provided in this repo to rebase this library.
The "com.google.common" package has been renamed to
"com.google.gwt.thirdparty.guava.common".

To build failureaccess-1.0.2-rebased.jar:

1) Download failureaccess-1.0.2.jar to failureaccess-1.0.2.jar

2a) Use the jarjar tool located at `lib/tonicsystems/jarjar-march-01-2024

2b) Rebase failureaccess-1.0.2.jar:
    <jarjar command> process failureaccess-1.0.2.jarjar-rules failureaccess-1.0.2.jar failureaccess-1.0.2-rebased.jar

3) Clean up the resulting jar to remove META-INF:
    zip failureaccess-1.0.2-rebased.jar -d META-INF/*
