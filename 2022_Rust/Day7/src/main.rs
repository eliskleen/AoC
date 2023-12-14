use std::cell::RefCell;
use std::{
    borrow::{Borrow, BorrowMut},
    ops::Deref,
};

fn main() {
    let contents = std::fs::read_to_string("data.txt").expect("this should work");
    let input = parse_input(contents);
    println!("{}", input.size);
    // part1(input.clone());
    // part2(input);
}
#[derive(Clone, Debug)]
struct FileTree {
    pub name: String,
    pub size: i32,
    pub parent: RefCell<Vec<FileTree>>,
    pub children: RefCell<Vec<FileTree>>,
}

fn part1(input: Vec<String>) {
    println!("Unimplemented")
}

fn part2(input: Vec<String>) {
    println!("Unimplemented")
}

fn parse_input(input: String) -> FileTree {
    let mut root = FileTree {
        name: "/".to_string(),
        size: 0,
        parent: RefCell::new(Vec::new()),
        children: RefCell::new(Vec::new()),
    };
    let mut current = &mut root.clone();
    // for line in input.lines().skip(1) {
    for index in 1..input.lines().count() {
        let line = input.lines().nth(index).unwrap();
        if line.starts_with("$ cd") {
            let target = line.split_whitespace().nth(2).unwrap();
            if target == ".." {
                current = current.parent.borrow_mut().last_mut().unwrap().borrow_mut();
            } else {
                let next = current
                    .children
                    .borrow_mut()
                    .iter_mut()
                    .find(|x| x.name == target);
                if next.is_some() {
                    current = next.unwrap();
                } else {
                    let mut new = FileTree {
                        name: target.to_string(),
                        size: 0,
                        parent: RefCell::new(vec![current.clone()]),
                        children: RefCell::new(Vec::new()),
                    };
                    current.children.borrow_mut().push(new);
                    current = current.children.borrow_mut().last_mut().unwrap();
                }
            }
        } else if line.starts_with("$ ls") {
            let mut size = 0;
            while index < input.lines().count() {
                let curr = input.lines().nth(index).unwrap();
                if curr.starts_with("$") {
                    break;
                }
                if !curr.starts_with("dir") {
                    size += curr
                        .split_whitespace()
                        .nth(1)
                        .unwrap()
                        .parse::<i32>()
                        .unwrap();
                }
            }
            current.size += size;
            add_size_to_parent(current, size);
        }
    }
    root
}
fn add_size_to_parent(node: &mut FileTree, size: i32) {
    if node.parent.borrow_mut().len() > 0 {
        node.parent.borrow_mut()[0].size += size;
        add_size_to_parent(node.parent.borrow_mut()[0].borrow_mut(), size);
    }
}
