use std::fs;

fn main() {
    let text = fs::read_to_string("input.txt").unwrap();

    let mut elves_inventory_summation:Vec<i32> = text.split("\n\n")
    .map(|inv|
        inv.split("\n").map(|n:&str|
            n.parse::<i32>().unwrap()
        ).sum()
    ).collect();

    elves_inventory_summation.sort_unstable();

    let part1:i32 = *elves_inventory_summation.iter().max().unwrap();
    let part2:i32 = elves_inventory_summation.iter().rev().take(3).sum();

    println!("Part 1: {}", part1 );
    println!("Part 2: {}", part2 );
}