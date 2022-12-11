#![feature(generators, generator_trait)]
/*
instr
*/
use std::ops::{Generator, GeneratorState};
use std::pin::Pin;

use crate::inputs::EXAMPLE;
mod inputs;
#[derive(Debug, Clone, Copy)]
struct RegFile {
    x: i32,
}

#[derive(Debug)]
enum Instr {
    Addx(i32),
    Noop,
}

impl Instr {
  fn gen(&self, mut reg: RegFile) -> Box<dyn Generator<Yield=RegFile, Return=RegFile>> {
    let instr = self.clone();
    let gen = move || {
      match instr {
        Instr::Addx(n) => {
          yield reg.clone();
          yield reg.clone();
          reg.x += n;
          return reg;
        },
        Instr::Noop => {
          yield reg.clone();
          return reg;
        },
      }
    };
    Box::new(gen)
  }
}

#[derive(Debug)]
struct State {
    reg: RegFile,
    instr: Instr,
}


fn parse(input: &str) -> Vec<Instr> {
    input
        .lines()
        .map(|line| {
            if line.starts_with("addx") {
                let n = line.strip_prefix("addx ").unwrap().parse::<i32>().unwrap();
                Instr::Addx(n)
            } else {
                Instr::Noop
            }
        })
        .rev()
        .collect()
}

fn run(input: &str) {
    let mut instrs: Vec<Instr> = parse(input);
    let mut state = State {
        reg: RegFile { x: 1 },
        instr: instrs.pop().unwrap(),
    };
}

fn main() {
  run(EXAMPLE);
}
