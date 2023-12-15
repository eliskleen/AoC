use std::collections::HashSet;
fn main() {
    let contents = std::fs::read_to_string("data.txt")
                        .expect("this should work");
    let input = parse_input(contents);
    part1(input.clone());
    part2(input);
}
fn find_index_of_distinct(n : usize, input : String) -> usize {
    for i in 0..input.len() {
        let slice = &input[i..(i + n)];
        let set = slice.chars().collect::<HashSet<char>>();
        if set.len() == n {
            return i + n;
        }
    }
    0
}
fn part1(input : String) {
    let index = find_index_of_distinct(4, input.clone());
    println!("Part 1: {}", index);
}

fn part2(input : String) {
    let index = find_index_of_distinct(14, input.clone());
    println!("Part 2: {}", index);
}
fn parse_input(input : String) -> String{ 
   input 
}