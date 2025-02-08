mod file_utils;
mod nmap;

use colored::*;
use file_utils::check_directory_exists;
use nmap::map_target;
use rand::Rng;
use std::io::{self, Write};
use std::net::IpAddr;
use std::str::FromStr;
use tokio::time::{sleep, Duration};

fn get_input(prompt: &str) -> String {
    let mut input = String::new();
    print!("{}", prompt);
    io::stdout().flush().unwrap();
    io::stdin()
        .read_line(&mut input)
        .expect(&"Failed to read input.".red());
    input.trim().to_string()
}

fn validate_ip(ip: &str) -> bool {
    match IpAddr::from_str(ip) {
        Ok(_) => true,
        Err(_) => false,
    }
}

fn validate_port(port: &str) -> bool {
    port.parse::<u16>().is_ok()
}

fn generate_number(min: i32, max: i32) -> i32 {
    let mut rng = rand::thread_rng();
    rng.gen_range(min..=max)
}

fn format_seconds(seconds: u64) -> String {
    let hours = seconds / 3600;
    let minutes = (seconds % 3600) / 60;
    let seconds = seconds % 60;
    format!("{:02}:{:02}:{:02}", hours, minutes, seconds)
}

async fn wait(seconds: u64) {
    let mut remaining_seconds = seconds;

    while remaining_seconds > 0 {
        let time_remaining = format_seconds(remaining_seconds);
        print!("{}", format!("\rWaiting for {}", time_remaining).yellow());
        io::stdout().flush().unwrap();
        sleep(Duration::from_secs(1)).await;
        remaining_seconds -= 1;
    }
    println!("{}", "\rRunning Next Scan...".yellow());
}

fn main() {
    let directory = get_input("\nOutput Directory: ");
    match check_directory_exists(&directory) {
        Ok(map_data_dir) => println!("NMAP Path: {}", map_data_dir.display().to_string().green()),
        Err(e) => eprintln!("Error: {}", e),
    }

    let target_ip = get_input("\nTarget IP: ");
    if !validate_ip(&target_ip) {
        eprintln!("Invalid IP Address...");
        return;
    }
    let target_port = get_input("Target Port (ENTER for All): ");
    if !target_port.is_empty() && !validate_port(&target_port) {
        eprintln!("Invalid Port...");
        return;
    }
    let file_prefix = get_input("Output File Prefix: ");
    let mode_choice = get_input("Choose Mode (Stealth / Fast): ").to_lowercase();

    let (min_wait_time, max_wait_time) = if mode_choice == "fast" {
        (0, 300)
    } else {
        (1800, 7200)
    };

    let rt = tokio::runtime::Runtime::new().unwrap();
    let scan_flags = [None, Some("-sS"), Some("-sF"), Some("-sN"), Some("-sT")];

    for i in 0..=4 {
        let flag = scan_flags.get(i % scan_flags.len()).copied().flatten();

        let _ = map_target(&target_ip, &target_port, flag, &directory, &file_prefix);

        let wait_time = generate_number(min_wait_time, max_wait_time);
        rt.block_on(wait(wait_time.try_into().unwrap()));
    }
}
