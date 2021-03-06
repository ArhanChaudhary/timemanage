/* 
The red line for all of the assignments follow a parabola
The first part of the setParabolaValues() function calculates the a and b values, and the second part handles the minimum work time and return cutoffs
this.funct(n) returns the output of an^2 + bn (with no c variable because it is translated to go through the origin)
set_mod_days() helps integrate break days into the schedule 
*/
Assignment.prototype.setParabolaValues = function() {
    /*
    The purpose of this function is to calculate these seven variables:
    a
    b
    cutoff_transition_value
    cutoff_to_use_round
    return_y_cutoff
    return_0_cutoff


    This part calculates a, b, and skew_ratio

    Three points are defined, one of which is (0,0), to generate a and b variables such that the parabola passes through all three of them
    This works because there is a parabola that exists that passes through any three chosen points (with different x coordinates)
    Notice how the parabola passes through the origin, meaning it does not use a c variable
    If the start of the line is moved and doesn't pass through (0,0) anymore, translate the parabola back to the origin instead of using a c variable
    Once the a and b variables are calculated, the assignment is retranslated accordingly

    The second point is (x1,y1), where x1 is the amount of days and y1 is the amount of units

    If set skew ratio is enabled, the third point is (x2,y2). skew_ratio will also be redefined
    If set skew ratio isn't enabled, the third point is now (1,x1/y1 * skew_ratio)
    Here, a straight line is connected from (0,0) and (x1,y1) and then the output of f(1) of that straight line is multiplied by the skew ratio to get the y-coordinate of the first point
    */
    // Define (x1, y1) and translate both variables to (0,0)
    let x1 = this.sa.x - this.red_line_start_x,
        y1 = this.sa.y - this.red_line_start_y;
    if (this.sa.break_days.length) {
        x1 -= Math.floor(x1 / 7) * this.sa.break_days.length + this.mods[x1 % 7];
    }
    // cite http://stackoverflow.com/questions/717762/how-to-calculate-the-vertex-of-a-parabola-given-three-points
    this.a = y1 * (1 - this.sa.skew_ratio) / ((x1 - 1) * x1);
    this.b = (y1 - x1 * x1 * this.a) / x1;
    if (!Number.isFinite(this.a)) {
        // If there was a zero division somewhere, where x2 === 1 or something else happened, make a line with the slope of y1
        this.a = 0;
        this.b = y1;
        this.cutoff_transition_value = 0;
        // Don't define cutoff_to_use_round because it will never be used if a = 0 and b = y1
        this.return_y_cutoff = x1 ? 1 : 0;
        this.return_0_cutoff = 0;
        return;
    }
    if (this.a <= 0 || this.b > 0) {
        var funct_zero = 0;
    } else {
        var funct_zero = precisionRound(-this.b / this.a, 10)
    }
    if (this.a >= 0) {
        var funct_y = x1;
    } else {
        var funct_y = precisionRound((Math.sqrt(this.b * this.b + 4 * this.a * y1) - this.b) / this.a / 2, 10);
    }
    if (this.sa.funct_round < this.sa.min_work_time) {
        this.cutoff_transition_value = 0;
        if (this.a) {
            this.cutoff_to_use_round = precisionRound((this.min_work_time_funct_round - this.b) / this.a / 2, 10) - 1e-10;
            if (funct_zero < this.cutoff_to_use_round && this.cutoff_to_use_round < funct_y) {
                // Same thing as:
                // const prev_output = clamp(0, this.funct(Math.floor(this.cutoff_to_use_round)), this.sa.y)
                // const output = clamp(0, this.funct(Math.ceil(this.cutoff_to_use_round)), this.sa.y)
                const prev_output = Math.min(Math.max(
                    this.funct(Math.floor(this.cutoff_to_use_round), false)
                , 0), this.sa.y),
                    output = Math.min(Math.max(
                        this.funct(Math.ceil(this.cutoff_to_use_round), false)
                    , 0), this.sa.y);
                if (output - prev_output) {
                    this.cutoff_transition_value = this.min_work_time_funct_round - output + prev_output;
                }
            }
        }
    }
    if (ignore_ends && this.sa.min_work_time) {
        var y_value_to_cutoff = y1;
    } else if (this.sa.funct_round < this.sa.min_work_time && (!this.a && this.b < this.min_work_time_funct_round || this.a && (this.a > 0) === (funct_y < this.cutoff_to_use_round))) {
        var y_value_to_cutoff = y1 - this.min_work_time_funct_round / 2;
    } else {
        var y_value_to_cutoff = y1 - this.min_work_time_funct_round + this.sa.funct_round / 2;
    }
    if (y_value_to_cutoff > 0 && this.sa.y > this.red_line_start_y && (this.a || this.b)) {
        if (this.a) {
            this.return_y_cutoff = (Math.sqrt(this.b * this.b + 4 * this.a * y_value_to_cutoff) - this.b) / this.a / 2;
        } else {
            this.return_y_cutoff = y_value_to_cutoff/this.b;
        }
        this.return_y_cutoff = precisionRound(this.return_y_cutoff, 10);
    } else {
        this.return_y_cutoff = 1;
    }
    if (this.return_y_cutoff < 2500) {
        if (this.return_y_cutoff < 1) {
            var output = 0;
        } else {
            // do ceil -1 instead of floor because ceil -1 is inclusive of ints; without this integer return cutoffs are glitchy
            for (let n = Math.ceil(this.return_y_cutoff - 1); n > 0; n--) {
                var output = this.funct(n, false);
                if (output <= this.sa.y - this.min_work_time_funct_round) {
                    break;
                }
                this.return_y_cutoff--;
            }
            if (this.return_y_cutoff <= 0) {
                this.return_y_cutoff++;
            }
        }
        if (ignore_ends && this.sa.min_work_time) {
            const lower = [this.return_y_cutoff, this.sa.y - output];

            let did_loop = false;
            for (let n = Math.floor(this.return_y_cutoff + 1); n < x1; n++) {
                const pre_output = this.funct(n, false);
                if (pre_output >= this.sa.y) {
                    break;
                }
                did_loop = true;
                output = pre_output;
                this.return_y_cutoff++;
            }
            if (did_loop) {
                const upper = [this.return_y_cutoff, this.sa.y - output];
                this.return_y_cutoff = [upper, lower][+(this.min_work_time_funct_round * 2 - lower[1] > upper[1])][0];
            }
        }
    }
    if (ignore_ends && this.sa.min_work_time) {
        var y_value_to_cutoff = 0;
    } else if (this.sa.funct_round < this.sa.min_work_time && (!this.a && this.b < this.min_work_time_funct_round || this.a && (this.a > 0) === (funct_zero < this.cutoff_to_use_round))) {
        var y_value_to_cutoff = this.min_work_time_funct_round / 2;
    } else {
        var y_value_to_cutoff = this.min_work_time_funct_round - this.sa.funct_round / 2;
    }

    if (y_value_to_cutoff < y1 && this.sa.y > this.red_line_start_y && (this.a || this.b)) {
        if (this.a) {
            this.return_0_cutoff = (Math.sqrt(this.b * this.b + 4 * this.a * y_value_to_cutoff) - this.b) / this.a / 2;
        } else {
            this.return_0_cutoff = y_value_to_cutoff / this.b;
        }
        this.return_0_cutoff = precisionRound(this.return_0_cutoff, 10);
    } else {
        this.return_0_cutoff = 0;
    }
    if (x1 - this.return_0_cutoff < 2500) {
        if (x1 - this.return_0_cutoff < 1) {
            var output = 0;
        } else {
            for (let n = Math.ceil(this.return_0_cutoff); n < x1; n++) {
                var output = this.funct(n, false);
                if (output >= this.min_work_time_funct_round + this.red_line_start_y) {
                    break;
                }
                this.return_0_cutoff++;
            }
            if (this.return_0_cutoff >= x1) {
                this.return_0_cutoff--;
            }
        }
        if (ignore_ends && this.sa.min_work_time) {
            const upper = [this.return_0_cutoff, output];

            let did_loop = false;
            for (let n = Math.floor(this.return_0_cutoff); n > 0; n--) {
                const pre_output = this.funct(n, false);
                if (pre_output <= this.red_line_start_y) {
                    break;
                }
                did_loop = true;
                var output = pre_output;
                this.return_0_cutoff--;
            }
            if (did_loop) {
                const lower = [this.return_0_cutoff, output];
                this.return_0_cutoff = [lower, upper][+(this.min_work_time_funct_round * 2 - upper[1] > lower[1])][0];
            }
        }
    }
}
Assignment.prototype.funct = function(x, translateX=true) {
    if (translateX === true) {
        // Translate x coordinate 
        x -= this.red_line_start_x;
        if (this.sa.break_days.length) {
            x -= Math.floor(x / 7) * this.sa.break_days.length + this.mods[x % 7];
        }
        if (x >= this.return_y_cutoff) return this.sa.y;
        if (x <= this.return_0_cutoff) return this.red_line_start_y;
    }
    if (this.sa.funct_round < this.sa.min_work_time && (!this.a && this.b < this.min_work_time_funct_round || this.a && (this.a > 0) === (x < this.cutoff_to_use_round))) {
        // Get translated y coordinate
        var output = this.min_work_time_funct_round * Math.round(x * (this.a * x + this.b) / this.min_work_time_funct_round);
        if (this.a < 0) {
            output += this.cutoff_transition_value;
        } else {
            output -= this.cutoff_transition_value;
        }
    } else {
        var output = this.sa.funct_round * Math.round(x * (this.a * x + this.b) / this.sa.funct_round);
    }
    // Return untranslated y coordinate
    // No point in untranslating x coordinate
    return precisionRound(output + this.red_line_start_y, max_length_funct_round);
}
Assignment.prototype.calcModDays = function() {
    let mods = [0],
        mod_counter = 0;
    for (let mod_day = 0; mod_day < 6; mod_day++) {
        if (this.sa.break_days.includes((this.assign_day_of_week + this.red_line_start_x + mod_day) % 7)) {
            mod_counter++;
        }
        mods.push(mod_counter);
    }
    return mods;
}