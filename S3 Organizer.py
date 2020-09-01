import boto3
from datetime import datetime

#thebucket = '' #removed for security reasons
#access_key = '' #removed for security reasons
#secret_key = '' #removed for security reasons

s3 = boto3.resource('s3')

BUCKET_NAME = "" #removed for security reasons
IMG_BUCKET = s3.Bucket(name=BUCKET_NAME)

def key_parser(raw_key=None):
    key = raw_key.split("/") #This will split key to before and after / : 10_09_2019 and the rest
    ASIN = key[1].split("_")[0] #This will take the second part, split the ASIN from everything after it, and keep the ASIN
    return ASIN

def filename_parser(raw_key=None):
    filename = raw_key.split("/")[1] #This will split key to before and after / : 10_09_2019 and the rest
    return filename

def update_key(obj):
    #If this works correctly "updating the key" is actually uploading the file with a new key, which means it will be placed in a different folder
    ASIN = key_parser(obj.key)
    filename = filename_parser(obj.key)
    new_key = "10_09_2019/" + ASIN + "/" + filename #This may add a second /
    return new_key
    #obj.put(Data=obj.data, Key=new_key)

def clean_obj(obj):
    # Approach 1
    obj.delete()
    
    # Approach 2
    #response = IMG_BUCKET.delete_objects( Delete={'Objects': [{'Key':obj.key},], 'Quiet':True},
    

def move_to_folder(obj):
    '''
    This function will do all of the grunt work of 'moving' a file: 
    Make a new key, 
    copy the original object, change the copy's key, 
    and delete the original object
    '''
    old_key = obj.key
    new_key = update_key(obj)
    
    #https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Bucket.copy
    copy_source = {'Bucket': BUCKET_NAME, 'Key': old_key}
    IMG_BUCKET.copy(copy_source, new_key)
    
    #Delete the original
    clean_obj(obj)
    
def not_already_organized(key):
    '''
    I am not sure how well this will do with already "organized" files, so
    this function will let us skip those.
    Unfortunately Hoyt has already started the process again and this isn't part of it.
    '''
    tmp = key.split("/")
    ret_bool = (tmp[0] == "10_09_2019" and len(tmp<3)
    return ret_bool
    
def main():
    start_time = datetime.time(datetime.now())
    i = 0
    k = 0
    for obj in IMG_BUCKET.objects.all():
        if obj.key[:11] == "10_09_2019/" and not_already_organized(obj.key): 
        #There's a lot of other junk in the folder right now, I only want things in 10_09_2019 folder
            move_to_folder(obj)
            i = (i + 1) % 10000 
            if i == 0:
                k = k+1
                print(str(datetime.time(datetime.now())) + "   " + str(k) + "0,000 files organized")
    end_time = datetime.time(datetime.now())
    print("\n\nDONE")
    print("Took: " + str(end_time - start_time))

if __name__=="__main__":
	main()
