fn main() {
    let contents = std::fs::read_to_string("data.txt")
        .expect("this should work");
    let input = parse_input(contents);
    part_1(input.clone());
    part_2(input);


}
fn part_1(input : Vec<Vec<i32>>) {
    let max_elf : i32 = input.iter().map(|c| c.iter().sum()).max().unwrap();
    println!("Part 1: {}", max_elf);
}

fn part_2(input : Vec<Vec<i32>>) {
    let mut elves = input.iter().map(|c| c.iter().sum()).collect::<Vec<i32>>();
    elves.sort_by(|a, b| b.cmp(a));
    let sum_3 = elves.into_iter().take(3).sum::<i32>();
    println!("Part 2: {}", sum_3);


}

fn parse_input(input : String) -> Vec<Vec<i32>> {
    input.split("\r\n\r\n")
                     .map(|l| l.split("\r\n")
                        .map(|i| i.parse().unwrap())
                        .collect::<Vec<i32>>())
                     .collect::<Vec<Vec<i32>>>()
}


