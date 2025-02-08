use colored::*;
use std::fs::create_dir_all;
use std::fs::File;
use std::io;
use std::path::{Path, PathBuf};

pub fn create_file(directory: &str, name: &str) -> io::Result<File> {
    let file_path = get_file_path(directory, name)?;

    if file_path.exists() {
        println!("{}", "File already exists.".red());
    } else {
        let file = File::create(&file_path)?;
        return Ok(file);
    }

    Ok(File::open(file_path)?)
}

pub fn get_file_path(directory: &str, name: &str) -> io::Result<PathBuf> {
    let mut path = PathBuf::from(directory);
    path.push(name);
    Ok(path)
}
/* Function's use will be implemented at a later date.
use std::fs::{create_dir_all, remove_file, File};

pub fn delete_file(file_path: &str) -> io::Result<()> {
    match remove_file(file_path) {
        Ok(_) => Ok(()),
        Err(e) => {
            println!("{}", e);
            Err(e)
        }
    }
}*/

pub fn check_directory_exists(dir_path: &str) -> io::Result<PathBuf> {
    let path = Path::new(dir_path).canonicalize()?;
    if !path.exists() {
        create_dir_all(&path)?;
    }
    Ok(path)
}
