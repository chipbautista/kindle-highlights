from dagster import op, Field


@op(
    config_schema={"upload_to_s3": Field(bool, default_value=False)},
    required_resource_keys={"s3_bucket"},
)
def save_topic_model(context, model_path: str):
    if not context.op_config["upload_to_s3"]:
        context.log.info(f"Skipping S3 upload")
        return

    s3_bucket = context.resources.s3_bucket
    filename = model_path.split("/")[-1]

    try:
        s3_bucket.upload_file(model_path, filename)
    except Exception as e:
        context.log.error(e)
        raise

    context.log.info(f"Topic model saved to s3://{s3_bucket._name}/{filename}.")
