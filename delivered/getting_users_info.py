    ############################################################################################
    ####################################  SCRIPT USAGE  ########################################
    ############################################################################################

############ This script is coded to get information of any user or user or all users in a particular group.
############
############ 1.==>  For users information we have to use a flag '--u' and then names for spedific USERS, 
############        as following.
############            sudo generate_data.py --u user_abc user_xyz ...
############ 
############ 2.==>  For getting information of all members of particular group we have to use a flag '--g'
############        and then name for spedific GROUP, as following.
############           sudo generate_data.py --g any_group_name
############ 
############ 3.==>  You can get help to by using any flag of '--help' of '-h', like
############          sudo generate_data.py -h  or 
    #############################################################################################

#  These are python modules used for different purposes.
import os                   #   To get system information
import pwd                  #   used for getting user information system database
import spwd                 #   This module is specifically used for getting sensitive information located in /etc/shadow file
import grp                  #   to get info about groups in a system

def get_user_passwd_data(username):     # This function get all information located in /etc/passwd file
    try:
        user_info = pwd.getpwnam(username)
        user_data = f"{user_info.pw_name}:{user_info.pw_passwd}:{user_info.pw_uid}:{user_info.pw_gid}:{user_info.pw_gecos}:{user_info.pw_dir}:{user_info.pw_shell}"
        return user_data                #   returning gathered information to store in a file
    except KeyError:
        return None                     #   if no info found against any unknown user then return 'None'
def get_user_shadow_data(username):     # Defining a function to get all information located in /etc/shadow file
    try:
        user_info = spwd.getspnam(username)
        user_data = f"{username}:{user_info.sp_pwd}:!:{user_info.sp_lstchg}:{user_info.sp_min}:{user_info.sp_max}:{user_info.sp_warn}:{user_info.sp_inact}:{user_info.sp_expire}:{user_info.sp_flag}"
        return user_data
    except KeyError:
        return None

def get_group_data(groupname):      #   This functino deals with getting info about all the users in a system
    try:
        group_info = grp.getgrnam(groupname)
        group_data = f"{group_info.gr_name}:{group_info.gr_passwd}:{group_info.gr_gid}:{','.join(group_info.gr_mem)}"
        return group_data
    except KeyError:
        return None

def generate_user_files(usernames, data_dir):
    passwd_data = ""                #   defining strings to how info received from /etc/passwd, /etc/shadow and group users
    shadow_data = ""
    group_data = ""

    for username in usernames:
        passwd_data += str(get_user_passwd_data(username)) + "\n"       #   appending data to respective strings
        shadow_data += str(get_user_shadow_data(username)) + "\n"
        group_data += str(get_group_data(username)) + "\n"

    with open(os.path.join(data_dir, "passwd.txt"), "w") as passwd_file:    #  writing to passwd.txt files all data related to passwd of users
        passwd_file.write(passwd_data)

    with open(os.path.join(data_dir, "shadow.txt"), "w") as shadow_file:        #  writing to shadow.txt files all data gather about users
        shadow_file.write(shadow_data)

    with open(os.path.join(data_dir, "group.txt"), "w") as group_file:      #  writing to group.txt files all data gather about group members
        group_file.write(group_data)

def main():
    import argparse         ###     This module if used for handling command line arguments provided by teh user while running script
    # import os

    parser = argparse.ArgumentParser(description="Generate user data files.")       #   Making an instance of argparse module
    parser.add_argument("--u", nargs="*", help="Provide user names to see info about users")    #    handling different options like for users or group_members
    parser.add_argument("--g", help="Enter group name to generate data for all users in specific group")

    args = parser.parse_args() 

    new_dir = "generated_data"      # generating a new directory to hold files (passwd, shadow and group fiels)
    try:
        os.mkdir(new_dir)
    except FileExistsError:
        pass
    os.chdir(new_dir)
    data_directory = os.getcwd()

    if not args.u and not args.g:
        print("\nSorry! You didn't provide any users or group name. Use \'--help\' or \'-h\' flag for usage.\n")
    else:
        if args.g:
            group_members = get_group_data(args.g).split(":")[-1].split(",")
            generate_user_files(group_members, data_directory)      #  calling function to generate files about users
        elif args.u:
            generate_user_files(args.u, data_directory)         # Calling function to generate files about group members
        else:
            print("--------------INVALID ARGUMENTS---------------------")       #   in case of wrong input by user

if __name__ == "__main__": 
    main()