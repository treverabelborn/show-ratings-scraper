# show-ratings-scraper

This project uses AWS SAM.


## Building

```bash
sam build
```

## Testing

Build your application first with the `sam build` command. Then use:

```bash
sam local start-lambda
```

Then in another terminal:

```bash
sam local invoke HelloWorldFunction
```

## Deploying

The application can be deployed to your AWS account with:

```bash
sam deploy
```
