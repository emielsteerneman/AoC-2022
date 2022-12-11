use std::fs;

fn main() {
    let file:String = fs::read_to_string("input.txt").unwrap();
    let lines:Vec<&str> = file.split("\n").collect();

    let games:Vec<[i32; 2]> = lines.iter().map( |line:&&str| {
        [line.chars().nth(0).unwrap() as i32 - 65, line.chars().nth(2).unwrap() as i32 - 88]
    }).collect();

    let part1:i32 = games.iter().map( | [a,b]:&[i32;2] | (3 * ((b - a + 4) % 3)) + b + 1 ).sum();
    let part2:i32 = games.iter().map( | [a,b]:&[i32;2] | (a + b + 2) % 3 + 1 + b * 3 ).sum();

    println!("Part 1: {}", part1);
    println!("Part 2: {}", part2);
}