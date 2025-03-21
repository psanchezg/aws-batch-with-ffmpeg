import boto3
#import requests
from urllib.parse import urlparse
#from aws_requests_auth.boto_utils import BotoAWSRequestsAuth

# Cloudformation output of the Amazon S3 bucket created by the solution : s3://batch-FFmpeg-stack-bucketxxxx/
s3_bucket_url = "s3://batch-ffmpeg-storage-stack-bucket43879c71-00aoewfcgmmk"
# Amazon S3 key of the media Asset uploaded on S3 bucket, to compute by FFmpeg command : test/myvideo.mp4
s3_key_input = "/2023/02/00146499/00146499.mp4"
# Amazon S3 key of the result of FFmpeg Command : test/output.mp4
s3_key_output = "/test/2023/02/00146499/%"
# EC2 instance family : `intel`, `arm`, `amd`, `nvidia`, `fargate`, `xilinx`
#compute = "fargate"
compute = "arm"
instance_type = "c7g.xlarge"
job_name = "fichero-00146499"

#output_file = "00146499_1.mp4"

output_file_options = [
    "-vf scale=640x360",
    "-c:v libx264",
    "-g 125",
    "-pix_fmt yuv420p",
    "-profile:v main",
    "-crf 20",
    "-maxrate 1000k",
    "-bufsize 5M",
	"-c:a aac",
    "-b:a 96k",
    "-movflags +faststart -write_tmcd 0 -fflags +genpts",
    "-y"
]
   
command={
    "name": job_name,
    #"global_options":  "",
    "input_url" : s3_bucket_url + s3_key_input,
    #"input_file_options" : "",
    "output_url" : s3_bucket_url + s3_key_output,
    "output_file_options": " ".join(output_file_options),
    "version": "1",
    "dashnames": "audioes,360p,720p"
}

# Deportes
#"dashnames": "audioes,low,med"

batch = boto3.client("batch")
result = batch.submit_job(
    jobName=job_name,
    jobQueue="arn:aws:batch:eu-west-1:054905228221:job-queue/batch-ffmpeg-job-queue-" + compute,
    jobDefinition="arn:aws:batch:eu-west-1:054905228221:job-definition/batch-ffmpeg-job-definition-" + compute,
    parameters=command,
    nodeOverrides={
        "nodePropertyOverrides": [
            {
                "targetNodes": "0,n",
                "containerOverrides": {
                    "instanceType": instance_type,
                },
            },
        ]
    },
)

print(result)
