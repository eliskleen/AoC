use std::ops::RangeInclusive;

fn main() {
    let contents = std::fs::read_to_string("data.txt")
                        .expect("this should work");
    let input = parse_input(contents);
    part1(input.clone());
    part2(input);
}



fn part1(input: Vec<Vec<Vec<u32>>>) {
    let mut overlaps = 0;
    for p in input {
        let p1 : Vec<u32> = p[0].clone();
        let p2 : Vec<u32> = p[1].clone();
        let add = p1.iter().all(|x| p2.contains(x)) || p2.iter().all(|x| p1.contains(x));
        if add {
            overlaps += 1;
        }
    }
    println!("Part 1: {}", overlaps)

}

fn part2(input : Vec<Vec<Vec<u32>>>) {
    let mut overlaps = 0;
    for p in input {
        let p1 : Vec<u32> = p[0].clone();
        let p2 : Vec<u32> = p[1].clone();
        let add = p1.iter().any(|x| p2.contains(x)) || p2.iter().any(|x| p1.contains(x));
        if add {
            overlaps += 1;
        }
    }
    println!("Part 2: {}", overlaps)

}

fn parse_input(input: String) -> Vec<Vec<Vec<u32>>>{
    let mut result = Vec::new();
    for line in input.lines() {
        let mut row = Vec::new();
        let r1 = get_range(line.split(',').collect::<Vec<&str>>()[0].to_string());
        let r2 = get_range(line.split(',').collect::<Vec<&str>>()[1].to_string());
        row.push(r1);
        row.push(r2);
        result.push(row);
    }
    result
}
fn get_range(pair : String) -> Vec<u32> {
    let s = pair.split('-').collect::<Vec<&str>>()[0].parse().unwrap();
    let e = pair.split('-').collect::<Vec<&str>>()[1].parse().unwrap();
    return (s..=e).collect();

}