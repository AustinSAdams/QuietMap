use crate::file_utils::create_file;
use anyhow::{Context, Result};
use colored::*;
use std::io::Write;
use std::process::Command;

pub fn map_target(
    ip: &str,
    port: &str,
    scan_type: Option<&str>,
    directory: &str,
    output_prefix: &str,
) -> Result<()> {
    let scan_type_str = match scan_type {
        Some("-sS") => "SYN",
        Some("-sF") => "FIN",
        Some("-sN") => "NULL",
        Some("-sT") => "CONNECT",
        None => "REGULAR",
        Some(_) => "",
    };

    let file_name = format!(
        "{PREFIX}_{TYPE}",
        PREFIX = output_prefix,
        TYPE = scan_type_str
    );
    match create_file(directory, &file_name) {
        Ok(mut file) => {
            let mut command = Command::new("sudo");

            command.arg("nmap");
            command.arg(ip);
            if let Some(f) = scan_type {
                command.arg(f);
            }
            if !port.trim().is_empty() {
                command.arg("-p").arg(port);
            }

            let output = command
                .output()
                .context("Failed to execute command".red())?;

            if output.status.success() {
                file.write_all(&output.stdout)
                    .expect(&"Failed to write output to file".red());
                println!(
                    "\nnmap {} {} {}",
                    ip,
                    scan_type.unwrap_or(""),
                    if port.trim().is_empty() {
                        "".to_string()
                    } else {
                        format!("-p {}", port)
                    }
                );

                println!("{}", format!("Output Stored In: {}.txt", file_name).green());
            } else {
                eprintln!(
                    "{}",
                    format!(
                        "Nmap command failed with error: {}",
                        String::from_utf8_lossy(&output.stderr)
                    )
                    .red()
                );
            }
        }
        Err(e) => eprintln!("{}", format!("Error creating file: {}", e).red()),
    }
    Ok(())
}
