use colored::*;
use std::env;
use std::fs::{create_dir_all, File};
use std::io;
use std::path::PathBuf;

pub fn create_file(name: &str) -> io::Result<File> {
    let file_path = get_file_path(name)?;

    if file_path.exists() {
        println!("{}", "File already exists.".red());
    } else {
        let file = File::create(&file_path)?;
        return Ok(file);
    }

    Ok(File::open(file_path)?)
}

pub fn get_file_path(name: &str) -> io::Result<PathBuf> {
    let mut path = env::current_dir()?;
    path.push("map_data");
    path.push(name);
    Ok(path)
}

pub fn check_directory_exists(dir_path: &str) -> io::Result<PathBuf> {
    let mut path = env::current_dir()?;
    path.push(dir_path);
    if !path.exists() {
        create_dir_all(&path)?;
    }
    Ok(path)
}
