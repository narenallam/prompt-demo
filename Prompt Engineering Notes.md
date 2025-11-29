# **Prompt Engineering: Master Guide (Generic)**

**Author:** _Naren Allam, 2005_

**Version:** 3.1 

**Target Models:** Generic (ChatGPT, Gemini, Claude, etc.)

**Target Audience:** Developers, Screenwriters, Engineering Managers, DevOps and Marketing Managers.

## **Table of Contents**

1. **Chapter 1: Foundations** \- What is it really? Mental models for LLMs.  
2. **Chapter 2: The Anatomy of a Prompt** \- Vague vs. Persona vs. Structured.  
3. **Chapter 3: The Zero-Shot Baseline** \- The essential "One Prompt" template.  
4. **Chapter 4: Few-Shot Prompting** \- Teaching by example.  
5. **Chapter 5: Chain of Thought (CoT)** \- Linear reasoning.  
6. **Chapter 6: Tree of Thoughts (ToT)** \- Branching strategy.  
7. **Chapter 7: Graph of Thoughts (GoT)** \- Networked constraints.  
8. **Chapter 8: Self-Reflection** \- The critique loop.  
9. **Chapter 9: Essential Short Patterns** \- Story, JSON, ReAct.  
10. **Chapter 10: Practice Workshop** \- 25 Drills across all domains.

## **Chapter 1: Foundations**

### **What is Prompt Engineering?**

**Practical Definition:** Prompt engineering is the craft of designing inputs to an LLM so that you systematically get **predictable, high-quality, reproducible outputs**.

Think of it as the difference between asking a junior developer "make the app faster" versus providing a detailed specification with performance benchmarks, profiling tools, and optimization strategies.

---

### **Mental Models for Understanding LLMs**

#### **Mental Model #1: The Probabilistic Pattern Machine**

**Key Insight:** An LLM doesn't "know" facts like a database. It predicts the next token based on statistical patterns learned from training data.

**Analogy:** Imagine an extremely sophisticated autocomplete system that has read the entire internet. When you type "The capital of France is...", it predicts "Paris" not because it has a geography database, but because that pattern appears billions of times in training data.

**Practical Implication:**

- ****Good:** "The Eiffel Tower is located in Paris, France. Based on this context, describe..."
- ****Risky:** Assuming it "knows" your company's internal database schema without providing it

**Example Demonstration:**

```markdown
## Vague Prompt (Unpredictable)
"Tell me about Python."

## Possible Outputs (High Variance)
- Output A: "Python is a snake species..."
- Output B: "Python is a programming language..."
- Output C: "Python was created by Guido van Rossum in 1991..."
```

The model doesn't "know" which Python you mean—it's predicting based on incomplete context.

```markdown
## Constrained Prompt (Predictable)
You are a programming language expert.

## TASK
Explain Python as a programming language to a JavaScript developer.

## OUTPUT FORMAT
1. Syntax comparison (3 key differences)
2. Use case strengths
3. One "gotcha" to watch out for
```

Now the output space is constrained to programming context with specific structure.

---

#### **Mental Model #2: Prompt = Constraints + Context**

**Key Insight:** A good prompt narrows the "search space" of possible next tokens. Without constraints, the LLM explores too many possibilities.

**Analogy:** It's like giving directions. "Go to the restaurant" is vague. "Take Highway 101 North, exit at University Ave, turn left, it's the Italian place next to the bookstore" is constrained.

**The Constraint Hierarchy:**

1. **Role/Persona** -> Sets domain expertise and tone
2. **Context** -> Provides necessary information
3. **Task Description** -> Defines what to do
4. **Output Format** -> Structures the response
5. **Examples** -> Shows the pattern (Few-Shot)
6. **Rules/Constraints** -> Explicit boundaries

**Example: Marketing Copy Generation**

```markdown
## Minimal Constraints (Weak)
"Write an ad for our product."

## Maximum Constraints (Strong)
## SYSTEM
You are a direct-response copywriter specializing in B2B SaaS.
You follow the AIDA framework (Attention, Interest, Desire, Action).

## CONTEXT
Product: CloudSecure - automated security compliance for healthcare companies
Target Audience: CTOs at 100-500 person healthcare startups
Pain Point: Manual SOC2 compliance takes 6 months and costs $200k

## TASK
Write a LinkedIn ad (150 words max)

## OUTPUT FORMAT
1. Headline (10 words max)
2. Body (hook -> problem -> solution -> CTA)
3. Call-to-Action button text

## CONSTRAINTS
- Use specific numbers
- Avoid buzzwords like "revolutionary" or "game-changing"
- Focus on time/cost savings
```

The second prompt constrains:

- **Who** (B2B SaaS copywriter)
- **What** (LinkedIn ad, 150 words)
- **How** (AIDA framework)
- **For Whom** (healthcare CTOs)
- **What to avoid** (buzzwords)

---

### **Why We Need Prompt Engineering**

Naive prompts lead to vague, inconsistent answers. In production systems, we need:

#### **1. Reliability: Same Input -> Similar Output**

**The Problem:**

```markdown
Prompt: "Summarize this customer review."
Input: "The product is okay but shipping was slow."

Run 1: "Mixed review."
Run 2: "Customer satisfied with product, unhappy with delivery speed."
Run 3: "Negative feedback regarding logistics."
```

**The Solution (With Structure):**

```markdown
## SYSTEM
You are a Customer Feedback Analyzer.

## INPUT
"The product is okay but shipping was slow."

## OUTPUT FORMAT (JSON)
{
  "product_sentiment": "positive|neutral|negative",
  "shipping_sentiment": "positive|neutral|negative",
  "overall_score": "number 1-5",
  "key_issue": "string or null"
}
```

Now every run produces structured, comparable output.

---

#### **2. Control: Specific Tone, Format, Safety Guardrails**

**Example: Engineering Manager Code Review Bot**

**Bad (No Control):**

```markdown
"Review this pull request."
```

Might produce: "This code is terrible. Did you even test this?"

**Good (With Guardrails):**

```markdown
## SYSTEM
You are a Senior Engineering Reviewer.

## TONE REQUIREMENTS
- Constructive, never dismissive
- Assume positive intent
- Ask questions instead of making accusations

## TASK
Review the code below for:
1. Logic errors
2. Security vulnerabilities
3. Performance concerns

## OUTPUT FORMAT
For each issue:
- Line number
- Issue type [Logic|Security|Performance]
- Explanation (2 sentences max)
- Suggested fix (code snippet)

## CONSTRAINTS
- If code is good, say "LGTM" with one positive note
- Never use words: "bad", "wrong", "stupid", "sloppy"
```

---

#### **3. Efficiency: Fewer Tokens, Less Back-and-Forth**

**Inefficient Conversation:**

```
User: "Help me fix this bug."
LLM: "What's the bug?"
User: "The login fails."
LLM: "What error do you see?"
User: "500 error."
LLM: "Can you share the logs?"
```

**Efficient Single Prompt:**

```markdown
## SYSTEM
You are a Backend Debugging Expert.

## BUG REPORT
Feature: User login
Error: HTTP 500 Internal Server Error
Endpoint: POST /api/auth/login
Logs:
[ERROR] 2024-01-15 10:23:45 - NullPointerException at AuthService.validateToken (Line 42)

## TASK
1. Identify root cause
2. Explain why it's happening
3. Provide fix with code snippet

## CONTEXT
Stack: Node.js + Express + PostgreSQL
Auth: JWT tokens
```

One prompt -> One comprehensive answer.

---

### **The API Mental Model**

**Think of prompts as APIs to a stochastic brain.**

| Traditional API | LLM Prompt API         |
| --------------- | ---------------------- |
| Function name   | Role/Persona           |
| Parameters      | Context + Input        |
| Return type     | Output Format          |
| Documentation   | Guidelines/Examples    |
| Error handling  | Constraints/Validation |

**Example: Traditional API**

```python
def calculate_discount(
    user_tier: str,  # "basic" | "premium" | "enterprise"
    cart_total: float,
    promo_code: str | None
) -> dict[str, float]:
    """Returns discount amount and final price"""
    pass
```

**Equivalent LLM Prompt API**

```markdown
## SYSTEM
You are a Pricing Calculator.

## INPUT SCHEMA
{
  "user_tier": "basic|premium|enterprise",
  "cart_total": "number",
  "promo_code": "string or null"
}

## OUTPUT SCHEMA
{
  "discount_amount": "number",
  "discount_percentage": "number",
  "final_price": "number",
  "savings_message": "string"
}

## RULES
- Basic: 0% discount
- Premium: 10% discount
- Enterprise: 15% discount
- Promo codes override tier discounts if higher
- SAVE20 = 20% off
- SAVE30 = 30% off

## INPUT
{{JSON_INPUT}}
```

---

### **Key Takeaways**

****LLMs are pattern predictors, not knowledge databases**  
****Prompts are constraints that narrow the output space**  
****Good prompting requires: Role + Context + Task + Format + Rules**  
****Production systems need reliability, control, and efficiency**  
****Think of prompts as API contracts with flexible execution**

---

### **Real-World Example: Startup Idea Validation**

**Before Prompt Engineering:**

```
"Help me with my startup idea."
```

-> Gets generic business advice

**After Prompt Engineering:**

```markdown
## SYSTEM
You are a seasoned startup mentor who has built and exited 3 SaaS companies.
You specialize in B2B marketplaces and have experience with:
- Product-market fit validation
- Unit economics
- Go-to-market strategy for two-sided platforms

## USER REQUEST
I want to build a marketplace connecting freelance videographers with small businesses that need promotional videos.

## CONTEXT
- Target customers: Small businesses (10-50 employees), e-commerce brands
- Supply side: Freelance videographers
- Geographic focus: US initially
- Problem: Businesses can't afford agency rates ($5k-$10k/video), freelancers on Fiverr are hit-or-miss quality

## GUIDELINES
- Think step-by-step through validation
- Explicitly list assumptions I should test
- Be honest about risks
- Prioritize actionable next steps

## OUTPUT FORMAT
1. Problem Summary (Is this a real pain point?)
2. Target User & Pain Points
3. Solution Hypothesis
4. Biggest Risks & Unknowns
5. Next 3 Concrete Actions (things I can do this week to validate)

## CONSTRAINTS
- Be concise but practical
- No generic advice like "talk to customers" without specifics
- Include specific questions I should ask potential customers
```

This prompt gives you structured, actionable insights instead of vague encouragement.

---

**Next Chapter Preview:** Now that you understand the foundations, Chapter 2 will show you the anatomy of a well-structured prompt with before/after examples.

## **Chapter 2: The Anatomy of a Prompt**

This chapter dissects prompt quality from worst to best, showing you the exact impact of each improvement. Think of it as upgrading from a crude hammer to precision tools.

---

### **2.1 The Vague Prompt (Bad Baseline)**

#### **Example:**

```
"Help me with my startup idea."
```

#### **Problems:**

- ****No role/persona** -> Model doesn't know what expertise to simulate
- ****No context** -> Model doesn't know your industry, stage, or constraints
- ****No structure** -> Output will be rambling and unfocused
- ****No constraints** -> Could give you anything from philosophical musings to generic platitudes

#### **Typical Output:**

```
That's great that you're thinking about starting a business! Having a startup 
can be very rewarding. What kind of idea do you have in mind? I'd be happy to 
discuss it with you. Some important things to consider are your target market, 
competition, and how you'll monetize. Feel free to share more details!
```

**Analysis:** Friendly but useless. It's asking YOU for information instead of providing value. This is the equivalent of calling a consultant and hearing "tell me more" 10 times.

---

### **2.2 The Persona-Based Prompt**

#### **Example:**

```
"You are a seasoned startup mentor who has built and exited 3 SaaS companies. 
Help me validate my startup idea."
```

#### **Improvement:**

- ****Sets domain expertise** -> Now thinks like a SaaS expert
- ****Establishes credibility** -> Answers from an experienced perspective
- ****Still lacks structure** -> No input format, no output format
- ****No specific task** -> "Validate" is vague

#### **Typical Output:**

```
As someone who's been through the startup journey three times, I can tell you 
that validation is crucial. The first thing you need to do is talk to potential 
customers. Don't fall in love with your solution—fall in love with the problem. 
I've seen too many founders build something nobody wants.

What's your idea? I'd be happy to give you my thoughts on the market opportunity, 
potential challenges, and whether there's a realistic path to product-market fit.
```

**Analysis:** Better tone and expertise, but still lacks structure. It's giving you philosophy instead of a framework. Output quality depends heavily on random variance.

---

### **2.3 The Fully Structured Prompt (The Gold Standard)**

#### **Why Structure Matters:**

Structure converts the LLM from a "conversation partner" into a **deterministic transformation function**. You're creating a contract:

- Input -> Must include X, Y, Z
- Processing -> Follow these rules A, B, C
- Output -> Must match format D

#### **Template:**

```markdown
## SYSTEM
You are a seasoned startup mentor who has built and exited 3 SaaS companies.
You specialize in {{SPECIFIC_DOMAIN}}.
Follow all rules strictly.

## USER REQUEST
{{USER_REQUEST}}

## CONTEXT
<<<CONTEXT>>>
(Provide all relevant details about your situation, market, constraints)

## GUIDELINES
- Think step-by-step
- Explicitly list assumptions you're making
- Ask for missing info if critical (max 3 questions)
- Be concise but practical
- Challenge ideas constructively

## OUTPUT FORMAT
1. Problem Summary (2-3 sentences)
2. Target User & Pain Points
3. Solution Hypothesis
4. Risks & Unknowns
5. Next 3 Concrete Actions (specific, actionable this week)

## CONSTRAINTS
- No generic advice
- Every recommendation must be tied to specific context provided
- If data is missing, state "Need to validate: [specific question]"
```

---

### **Real Example: Startup Validation**

```markdown
## SYSTEM
You are a seasoned startup mentor who has built and exited 3 SaaS companies.
You specialize in B2B marketplaces and have experience with:
- Product-market fit validation
- Two-sided marketplace dynamics
- Unit economics for platforms

Follow all rules strictly.

## USER REQUEST
Help me validate whether this startup idea is worth pursuing full-time.

## CONTEXT
Idea: Marketplace connecting freelance videographers with small businesses for promotional videos.

Target Customers:
- Small businesses (10-50 employees)
- E-commerce brands needing product videos
- Local service businesses (dentists, gyms, etc.)

Supply Side:
- Freelance videographers
- Budget: $500-$2000 per video (vs $5k-$10k agency rates)

My Background:
- Former product manager at Uber (2 years)
- No video production experience
- $50k savings to bootstrap
- Located in Austin, TX

Current Traction:
- None. This is just an idea.

## GUIDELINES
- Think step-by-step through validation
- Explicitly list assumptions I should test
- Be honest about risks, especially red flags
- Prioritize actions by impact/effort ratio

## OUTPUT FORMAT
1. Problem Summary (Is this a real pain point worth solving?)
2. Target User & Pain Points
3. Solution Hypothesis & Market Positioning
4. Biggest Risks & Red Flags
5. Next 3 Concrete Actions (things I can do THIS WEEK to validate)

## CONSTRAINTS
- No generic advice like "talk to customers" without specifics
- Include specific questions I should ask potential customers
- If this idea has fatal flaws, say so directly
```

#### **Expected Output:**

```markdown
## 1. PROBLEM SUMMARY
There IS a real pain point: small businesses need video content for social/web 
but can't afford $5-10k agency rates. However, you're entering a crowded space 
(Fiverr, Upwork, Thumbtack already serve this market). Your differentiation must 
be crystal clear or you'll be commoditized immediately.

## 2. TARGET USER & PAIN POINTS
Primary Target: E-commerce brands (10-50 employees) with $1M-$10M revenue

Pain Points:
- Fiverr quality is inconsistent (50% of videos are unusable)
- Agencies are too expensive for their volume needs (they need 4-8 videos/month)
- Finding/vetting freelancers takes 10+ hours per hire
- No easy way to build ongoing relationships with creators

Secondary Target: Local service businesses (gyms, dentists)
Pain: Same as above, but lower willingness to pay ($500 vs $2000)

## 3. SOLUTION HYPOTHESIS & POSITIONING
Hypothesis: "Vetted marketplace with quality guarantees"

Positioning Options:
A) "The Thumbtack for video" -> Dangerous, low differentiation
B) "Quality-guaranteed video at 1/3 agency cost" -> Better, but requires robust vetting
C) "Subscription video service with dedicated creator matching" -> Best, recurring revenue

Recommended: Position as "Fractional video team" - businesses pay $2-3k/month for 
4 videos via dedicated videographer relationship.

## 4. BIGGEST RISKS & RED FLAGS
** RED FLAG: You have no video production domain expertise
  - Risk: You can't vet quality, spot bad work, or advise creators
  - Mitigation: Partner with a video producer as co-founder

** RISK: Two-sided marketplace cold start problem
  - Classic chicken-egg: need videos to attract businesses, need clients to attract videographers
  - Mitigation: Start supply-first (easier to recruit creators than customers)

** RISK: Low margins in crowded market
  - If you take 20% commission on $1500 video = $300 revenue
  - Need 167 videos/month to hit $50k MRR
  - Without differentiation, you'll compete on price and die

** ASSUMPTION TO TEST: Do businesses actually hate Fiverr/Upwork enough to pay a premium?
** ASSUMPTION TO TEST: Will videographers join another marketplace when they're already on 5+ platforms?

## 5. NEXT 3 CONCRETE ACTIONS (THIS WEEK)

### Action 1: Customer Discovery (10 conversations)
Target: E-commerce brand owners/marketing managers in Austin
Questions to ask:
- "How do you currently get video content made? Walk me through last time."
- "What was frustrating about that process?"
- "If there was a service that guaranteed quality video for $1500, delivered in 5 days, would you try it?"
- "How often do you need new videos?" (validate frequency)
- DON'T pitch. Just listen.

Where to find them: Austin Digital Marketing meetup, local Shopify merchants group

### Action 2: Supply-Side Research (5 videographer interviews)
Find: Freelancers currently on Fiverr/Upwork making $50k-$150k/year
Questions:
- "What % of leads from Fiverr actually close?"
- "What do you wish was different about these platforms?"
- "Would you pay 15% commission for guaranteed monthly clients?"

Where: Austin Freelancers Facebook group, local creator meetups

### Action 3: Competitive Analysis
Task: Book 3 videos on Fiverr ($150 each = $450 total)
- Experience the customer journey yourself
- Document: Time to find vendor, quality variance, communication friction
- Compare: What would make your platform 10x better at each step?

Note: Don't spend more than $450 or 20 hours this week. If you can't find 10 
people willing to talk about their video pain, this market doesn't care enough.
```

---

### **Key Differences: Vague vs. Structured**

| Aspect              | Vague Prompt        | Structured Prompt                                    |
| ------------------- | ------------------- | ---------------------------------------------------- |
| **Clarity**         | "Help me"           | "Validate this specific idea against these criteria" |
| **Expertise**       | Generic             | Domain-specific (B2B marketplaces)                   |
| **Context**         | None                | Detailed (idea, background, constraints)             |
| **Output**          | Unpredictable       | 5-section structured analysis                        |
| **Actionability**   | Philosophy          | Concrete next steps with specifics                   |
| **Reproducibility** | Low (high variance) | High (consistent structure)                          |

---

### **The Anatomy Breakdown**

Every production-grade prompt should have these components:

```markdown
## SYSTEM (Role & Expertise)
Who is the LLM pretending to be? What's their background?

## TASK (Explicit Instruction)
What exactly should they do?

## CONTEXT (All Relevant Info)
What information do they need to do it well?

## GUIDELINES (Process Instructions)
How should they approach the task?

## OUTPUT FORMAT (Structure)
What should the answer look like?

## CONSTRAINTS (Boundaries)
What should they NOT do? What are the rules?
```

**Pro Tip:** Use delimiters like `## SECTION` or `<<<CONTEXT>>>` to make prompts easier to parse and modify programmatically.

---

### **More Examples Across Domains**

#### **Example: Engineering Manager (Code Review)**

```markdown
## SYSTEM
You are a Senior Backend Engineer with 10 years experience in distributed systems.
You specialize in Python microservices and PostgreSQL performance.

## TASK
Review the following code for production readiness.

## CODE

def get_user_orders(user_id):
    orders = db.query(f"SELECT * FROM orders WHERE user_id = {user_id}")
    return orders

## GUIDELINES
- Check for security vulnerabilities
- Identify performance issues
- Suggest best practices
- Be constructive, not condescending

## OUTPUT FORMAT
1. Security Issues (with severity: Critical/High/Medium/Low)
2. Performance Concerns
3. Code Quality Improvements
4. Refactored Code Example

## CONSTRAINTS
- Assume production database with 10M orders
- Code must handle 1000 req/sec
```

#### **Example: Marketing Manager (Email Campaign)**

```markdown
## SYSTEM
You are a Direct Response Copywriter specializing in B2B SaaS email campaigns.
You've written emails with average open rates of 35% and CTR of 8%.

## TASK
Write a re-engagement email for users who haven't logged in for 30 days.

## CONTEXT
Product: Project management tool
Audience: Product managers at startups
Last activity: Created 2 projects, invited 1 team member, then went silent
Hypothesis: They got busy and forgot, OR found the onboarding confusing

## GUIDELINES
- Use curiosity + urgency (but not fake urgency)
- Provide value upfront (not just "come back please")
- Include social proof

## OUTPUT FORMAT
1. Subject Line (3 variants to A/B test)
2. Preview Text (50 chars max)
3. Email Body (150 words max)
4. CTA Button Text

## CONSTRAINTS
- No discounts (we don't compete on price)
- Tone: Helpful colleague, not desperate salesperson
- Must work on mobile (65% of opens)
```

---

### **Chapter 2 Takeaways**

****Vague prompts** -> Unpredictable, generic outputs  
****Persona prompts** -> Better expertise, still inconsistent  
****Structured prompts** -> Reliable, actionable, reproducible  
****Always include**: Role, Task, Context, Guidelines, Format, Constraints  
****Use delimiters** -> Makes prompts parsable and modular

---

**Next Chapter Preview:** Chapter 3 will show you the Zero-Shot Baseline—how to get great results from a single prompt when you have no examples to show.

## **Chapter 3: The Zero-Shot Baseline**

### **What is Zero-Shot Prompting?**

Zero-shot prompting is the technique of getting high-quality outputs from an LLM **without providing any examples**. You rely entirely on clear instructions, role definition, and output structure to guide the model.

This is your baseline technique—master this before moving to Few-Shot or Chain of Thought patterns.

---

### **When to Use Zero-Shot**

**Use zero-shot prompting when:**

- **You have no examples** to show the model
- **The task is well-defined** and commonly understood (summarization, translation, analysis)
- **You need quick iteration** without curating example sets
- **The output varies significantly** by input (can't template with examples)
- **You're prototyping** before investing in Few-Shot examples

**Don't use zero-shot when:**

- The task requires specific formatting that's hard to describe (use Few-Shot instead)
- The model consistently misinterprets your instructions (add examples)
- You need extremely consistent output structure (Few-Shot is more reliable)

---

### **Why Zero-Shot Works**

Modern LLMs are trained on vast corpora including:

- Technical documentation
- Q&A forums (Stack Overflow, Quora)
- Academic papers
- Code repositories
- Professional writing

When you say "You are a Senior Backend Engineer", the model activates patterns learned from thousands of engineering discussions. You're essentially indexing into its training distribution.

**Key Principle:** The clearer your role definition and constraints, the narrower the probability distribution of outputs.

---

### **The Zero-Shot Template**

```markdown
## SYSTEM
You are an expert {{ROLE}}. 
Follow all rules strictly.

## TASK
{{TASK_DESCRIPTION}}

## INPUT
<<<INPUT>>>

## CONSTRAINTS
- Domain: {{DOMAIN}}
- Length: {{LENGTH_LIMIT}}
- Style: {{STYLE}}
- If information is missing, ask at most 3 clarification questions

## OUTPUT FORMAT
1. Summary (3-5 bullet points)
2. Detailed Answer
3. Assumptions
4. Limitations / What You Don't Know
```

---

### **Real-World Examples**

#### **Example 1: Engineering Manager (Incident Triage)**

**Use Case:** Quickly assess production incidents without historical examples.

```markdown
## SYSTEM
You are a Site Reliability Engineer (SRE) with 8 years experience in distributed systems.
You specialize in incident triage and root cause analysis.

## TASK
Assess the severity and urgency of the following production incident.

## INPUT
Service: Payments API
Error: Intermittent 503 errors
Frequency: 15% of requests failing
Started: 10 minutes ago
Recent changes: Database migration deployed 2 hours ago
User impact: Customers cannot complete checkout

## CONSTRAINTS
- Classify severity as: P0 (critical), P1 (high), P2 (medium), P3 (low)
- Provide initial hypothesis within 2 minutes
- If you need more data to determine severity, specify exactly what to check

## OUTPUT FORMAT
1. Severity Classification (P0-P3 with justification)
2. Immediate Actions (next 3 steps in priority order)
3. Information Needed (specific metrics, logs, or tests to run)
4. Estimated Time to Resolution (best/worst case)
```

**Expected Output:**

```
1. SEVERITY CLASSIFICATION: P0 (Critical)

Justification:
- Payment system is core revenue-generating functionality
- 15% failure rate means significant revenue loss ($X per minute)
- Started after database migration suggests clear correlation
- User-facing impact (cannot complete purchases)

2. IMMEDIATE ACTIONS

Priority 1: Check database connection pool exhaustion
- Action: Query current active connections vs pool size
- Command: `SELECT count(*) FROM pg_stat_activity WHERE state = 'active'`
- Hypothesis: Migration increased query complexity, exhausting connections

Priority 2: Enable database query logging
- Action: Set log_min_duration_statement = 1000ms to catch slow queries
- Reason: Identify if migration introduced performance regression

Priority 3: Prepare rollback plan
- Action: Verify backup exists and test rollback procedure in staging
- Timeline: Should be ready to execute within 10 minutes if issues persist

3. INFORMATION NEEDED

Critical metrics to collect:
- Database CPU/memory utilization (last 3 hours)
- Payment API response time p50/p95/p99 (compare pre/post migration)
- Active database connection count over time
- Error rate by specific endpoint (is it isolated to one query?)

Specific logs:
- Stack traces from 503 errors (check for connection timeout vs query timeout)
- Migration script execution logs (did it complete successfully?)

4. ESTIMATED TIME TO RESOLUTION

Best case: 15-30 minutes (if simple config change like increasing connection pool)
Worst case: 2-4 hours (if migration introduced data corruption requiring rollback)

Recommendation: If issue not identified within 20 minutes, execute rollback.
```

---

#### **Example 2: Marketing Manager (Ad Copy Generation)**

**Use Case:** Create platform-specific ad copy without examples.

```markdown
## SYSTEM
You are a Performance Marketing Copywriter specializing in B2B SaaS.
You understand platform-specific best practices for LinkedIn, Google Ads, and Facebook.

## TASK
Write three ad variations for different platforms promoting our product launch.

## CONTEXT
Product: DevSecure - Automated security testing for CI/CD pipelines
Target Audience: Engineering Managers and CTOs at 50-500 person tech companies
Key Value Prop: Find security vulnerabilities before production, not after
Price Point: $299/month per team
Competition: Snyk, Checkmarx (but we're 60% cheaper)

## CONSTRAINTS
- LinkedIn: Professional tone, 150 characters max
- Google Search: Focus on intent (they're searching for solution)
- Facebook: Conversational, can use light humor

## OUTPUT FORMAT
For each platform provide:
1. Headline
2. Ad body
3. Call-to-action
4. Targeting note (what keyword/audience to target)
```

**Expected Output:**

```
LINKEDIN AD

Headline: Stop Security Vulnerabilities Before They Reach Production

Body:
DevSecure integrates with your CI/CD pipeline to catch security issues in pull requests—not customer bug reports. Engineering teams at mid-size tech companies save 15+ hours/week on security remediation. Starting at $299/month.

Call-to-Action: Start Free Trial

Targeting Note: Target job titles "Engineering Manager", "VP Engineering", "CTO" at companies 50-500 employees in Technology industry.

---

GOOGLE SEARCH AD

Headline: Automated Security Testing for CI/CD | DevSecure

Body:
Catch vulnerabilities before deployment. Integrates with GitHub, GitLab, Bitbucket. 14-day free trial. No credit card required. Trusted by 300+ engineering teams.

Call-to-Action: Try Free for 14 Days

Targeting Note: Keywords - "CI/CD security testing", "automated security scan", "DevSecOps tools", "security testing pipeline"

---

FACEBOOK AD

Headline: Your code passes tests. But does it pass security?

Body: 
Shipping fast is great. Shipping vulnerable code? Not so much. DevSecure scans every PR for security issues before your team even clicks merge. Same tool used by engineering teams at [recognizable customer]. And it's way cheaper than fixing breaches later.

Call-to-Action: See How It Works

Targeting Note: Retargeting audience - people who visited pricing page but didn't start trial. Also lookalike audience based on current customer list.
```

---

#### **Example 3: Screenwriter (Scene Analysis)**

**Use Case:** Analyze script scenes for pacing issues.

```markdown
## SYSTEM
You are a Script Doctor specializing in thriller and mystery screenplays.
You have 15 years of experience analyzing scene structure, pacing, and tension.

## TASK
Analyze the following scene for pacing and tension issues.

## SCENE
INT. DETECTIVE'S OFFICE - DAY

Detective Sarah sits at her desk reviewing case files. She flips through pages slowly. Her partner Tom enters with coffee.

TOM
Morning. Any luck with the files?

SARAH
Nothing yet. These victims have nothing in common.

TOM
Maybe that's the point? Randomness?

SARAH
No. There's always a pattern. We just haven't found it.

She continues reading. Tom drinks his coffee. Long pause. Sarah suddenly stops.

SARAH (CONT'D)
Wait. They all went to the same college.

TOM
Which one?

SARAH
Westfield University. Class of 2008.

## CONSTRAINTS
- Focus on pacing and tension
- Identify specific line or beat that drags
- Suggest concrete improvements

## OUTPUT FORMAT
1. Pacing Assessment (score 1-10)
2. Identified Issues
3. Suggested Revision (rewrite specific portion)
4. Technique Used (explain why your change works)
```

**Expected Output:**

```
1. PACING ASSESSMENT: 4/10

This scene has the right information payoff (the college connection) but takes too long to get there. The middle section drags significantly.

2. IDENTIFIED ISSUES

Issue A: "She continues reading. Tom drinks his coffee. Long pause."
Problem: Dead air. No tension, no character development, no visual interest. This is "waiting room" pacing in a thriller.

Issue B: The dialogue reveals the twist too easily
Problem: Sarah finds the connection without struggle. No failed attempts, no red herrings. The audience won't feel the character's breakthrough because there was no obstacle.

Issue C: Tom is passive
Problem: He's just asking questions. Give him conflicting information or urgency to create tension.

3. SUGGESTED REVISION

Replace the middle section:

---
SARAH
No. There's always a pattern.

She slams the file shut, frustrated. Stands. Walks to the evidence board.

TOM
Captain wants an update in 20 minutes. What do I tell him?

SARAH
(not looking at him)
Tell him we're following leads.

TOM
We don't have leads, Sarah.

She stares at the board. Three victim photos. Different ages, different cities.

SARAH
(eyes narrowing)
Tom... hand me the Johnson file.

TOM
Why? You already looked at—

SARAH
Just hand it to me.

She flips to the first page. Her face changes.

SARAH (CONT'D)
Westfield University.

She grabs the second file. Flips.

SARAH (CONT'D)
Westfield. Class of 2008.

TOM
You think they knew each other?

4. TECHNIQUE USED

A) Added time pressure: "Captain wants an update in 20 minutes"
Creates external urgency beyond solving the case.

B) Physical movement: Sarah moves to the evidence board
Gives the scene visual variety and shows her thought process physically.

C) Discovery through action: She flips through files frantically
The audience sees her realization build, rather than stated flat. More cinematic.

D) Tom provides resistance: "We don't have leads"
His skepticism makes Sarah's breakthrough feel earned, not convenient.
```

---

### **Zero-Shot vs. Few-Shot Decision Matrix**

| Situation              | Use Zero-Shot                                | Use Few-Shot                  |
| ---------------------- | -------------------------------------------- | ----------------------------- |
| **Task complexity**    | Common tasks (summarize, analyze, translate) | Uncommon/specialized formats  |
| **Output consistency** | Variance acceptable                          | Must be identical structure   |
| **Setup time**         | Need results immediately                     | Can invest time in examples   |
| **Domain knowledge**   | Well-known domain (programming, marketing)   | Niche domain (legal, medical) |
| **Error tolerance**    | Can iterate and refine                       | Must be right first time      |

---

### **Best Practices for Zero-Shot Prompts**

1. **Be Specific with the Role**
    - Bad: "You are a developer"
    - Good: "You are a Senior Backend Engineer with expertise in Python microservices and PostgreSQL optimization"

2. **Provide Domain Context**
    - Don't assume the model knows your company/product
    - Include relevant background in the CONTEXT section

3. **Define Output Structure**
    - Unstructured outputs are hard to parse
    - Use numbered lists, JSON schemas, or clear sections

4. **Set Explicit Constraints**
    - Word count limits
    - Tone requirements
    - Things to avoid

5. **Request Transparency**
    - Ask for assumptions
    - Ask what information is missing
    - This prevents confidently wrong answers

---

### **Common Zero-Shot Mistakes**

**Mistake 1: Vague Task Description**

```
Bad: "Analyze this code"
Good: "Analyze this code for security vulnerabilities, focusing on SQL injection and authentication bypass risks"
```

**Mistake 2: No Output Format**

```
Bad: "Tell me about performance issues"
Good: "List performance issues in priority order (P0-P2), with specific line numbers and suggested fixes"
```

**Mistake 3: Assuming Context**

```
Bad: "Review the recent changes"  (What changes? Model doesn't know)
Good: [Include the actual changes in the prompt]
```

---

### **Key Takeaways**

* Zero-shot is your baseline—use it when you don't have examples
* Success depends on clear role definition, task description, and output structure
* Works best for common tasks in well-understood domains
* If you find yourself reformulating the same prompt repeatedly, switch to Few-Shot
* Always specify what you DON'T want, not just what you want

---

**Next Chapter Preview:** Chapter 4 covers Few-Shot Prompting—teaching the model by example when Zero-Shot isn't precise enough.

## **Chapter 4: Few-Shot Prompting**

### **What is Few-Shot Prompting?**

Few-shot prompting is the technique of teaching an LLM by showing it labeled examples of the desired input-output pattern. Instead of describing what you want, you **show** the model 2-5 examples, and it learns to imitate the pattern.

This is the most reliable technique for tasks requiring precise formatting, consistent structure, or domain-specific transformations.

---

### **How Few-Shot Learning Works**

LLMs learn patterns during training, but few-shot prompting allows them to learn task-specific patterns **at inference time** by recognizing the structure in your examples.

**Mental Model:** Think of it like training a junior employee. Instead of writing a 10-page manual on "How to Write Bug Reports," you show them 3 examples of good bug reports. They pattern-match and replicate the structure.

**Key Mechanism:** The model performs in-context learning—it doesn't update weights, but it adjusts its attention patterns based on your examples to predict outputs that match the demonstrated format.

---

### **When to Use Few-Shot Prompting**

**Use few-shot when:**

- **Precise formatting is required** - Converting data to specific structures (JSON schemas, code formats, report templates)
- **Zero-shot fails** - The model misinterprets your text instructions
- **Domain-specific transformations** - Style transfer, dialect translation, code refactoring patterns
- **Classification tasks** - Especially with custom categories
- **Consistency is critical** - Need identical output structure across multiple inputs

**Don't use few-shot when:**

- Examples are hard to create or don't exist
- Task is simple enough for zero-shot (wastes tokens)
- Output varies wildly based on input (examples won't generalize)
- You need reasoning transparency (Few-Shot can feel like a black box; use Chain of Thought instead)

---

### **Few-Shot vs. Zero-Shot: When to Choose Each**

| Factor            | Zero-Shot                          | Few-Shot                                   |
| ----------------- | ---------------------------------- | ------------------------------------------ |
| **Output format** | Flexible, described in words       | Strict, shown by example                   |
| **Setup time**    | Immediate                          | Requires curating examples                 |
| **Consistency**   | Medium (variance possible)         | High (mimics examples)                     |
| **Token cost**    | Lower (no examples)                | Higher (examples in every call)            |
| **Best for**      | Analysis, reasoning, brainstorming | Formatting, classification, transformation |

---

### **The Few-Shot Template**

```markdown
## SYSTEM
You are an expert {{ROLE}}.
Learn the pattern from the examples and apply it strictly to new inputs.

## EXAMPLES

### Example 1
**Input:** {{INPUT_1}}
**Output:** {{OUTPUT_1}}

### Example 2
**Input:** {{INPUT_2}}
**Output:** {{OUTPUT_2}}

### Example 3
**Input:** {{INPUT_3}}
**Output:** {{OUTPUT_3}}

---

## NEW INPUT
{{NEW_INPUT}}

## REQUIRED OUTPUT
Use exactly the same format and structure as the examples above.
```

---

### **How Many Examples to Provide?**

**General Guidelines:**

- **2-3 examples**: Sufficient for most formatting tasks
- **4-5 examples**: For complex patterns or edge cases
- **1 example** (one-shot): Risky, only if the pattern is extremely simple
- **6+ examples**: Diminishing returns; consider fine-tuning instead

**Quality > Quantity:** Better to have 3 diverse, well-chosen examples than 10 similar ones.

**Diversity matters:** Show edge cases:

- Example 1: Standard case
- Example 2: Edge case (missing data, special characters)
- Example 3: Another variation

---

### **Example 1: Engineering Manager (Ticket Triage)**

**Use Case:** Auto-classify incoming support tickets into categories with priority levels.

```markdown
## SYSTEM
You are a Technical Program Manager for a B2B SaaS company.
Classify incoming support tickets into categories and assign priority levels.

## EXAMPLES

### Example 1
**Input:** "The login page is showing a 500 error for all users. Nobody can access the app."
**Output:** 
{
  "category": "Critical Bug",
  "priority": "P0",
  "severity": "blocker",
  "affected_users": "all",
  "reason": "Complete service outage preventing all access"
}

### Example 2
**Input:** "It would be great if we could export reports to Excel instead of just PDF."
**Output:**
{
  "category": "Feature Request", 
  "priority": "P2",
  "severity": "enhancement",
  "affected_users": "subset",
  "reason": "Quality of life improvement, workaround exists"
}

### Example 3
**Input:** "The dashboard loads slowly when there are more than 1000 records. Takes about 30 seconds."
**Output:**
{
  "category": "Performance Issue",
  "priority": "P1",
  "severity": "degraded",
  "affected_users": "power_users",
  "reason": "Significant UX impact for high-volume customers, likely needs query optimization"
}

---

## NEW INPUT
"When users try to upload files larger than 50MB, they get a timeout error after 2 minutes."
```

**Expected Output:**

```json
{
  "category": "Bug",
  "priority": "P1",
  "severity": "major",
  "affected_users": "subset",
  "reason": "File upload is core functionality; affects users with legitimate large files; workaround exists but poor UX"
}
```

---

### **Best Practices**

1. **Choose Representative Examples** - Cover common cases and at least one edge case

2. **Maintain Consistent Format** - All examples must use identical structure

3. **Be Explicit About Output Format**

```markdown
## REQUIRED OUTPUT
Use EXACTLY the same format as examples.
Match the JSON schema precisely.
```

4. **Order Matters** - Put clearest example first, edge cases later

5. **Balance Trade-offs** - More examples = better accuracy but higher token cost

---

### **Common Mistakes**

**Mistake 1: Inconsistent Examples**

```
Bad: Example 1 (JSON), Example 2 (prose), Example 3 (different schema)
Good: All examples follow identical format
```

**Mistake 2: Examples Too Similar**

```
Bad: Three examples all showing success scenarios
Good: Example 1 (success), Example 2 (error), Example 3 (edge case)
```

**Mistake 3: Token Waste**

```
Bad: 10 examples for simple task
Good: 2-3 examples for simple, 4-5 for complex
```

---

### **Key Takeaways**

* Few-shot learning teaches by example, not instruction
* Use when formatting precision matters or zero-shot fails
* 3-5 examples is the sweet spot for most tasks
* Examples must be consistent and representative
* Higher token cost than zero-shot, but more reliable for structured output

---

**Next Chapter Preview:** Chapter 5 introduces Chain of Thought—making the model show its reasoning step-by-step for complex logic.


## **Chapter 5: Chain of Thought (CoT)**

### **What is Chain of Thought Prompting?**

Chain of Thought (CoT) is a prompting technique that instructs the LLM to show its reasoning process step-by-step before arriving at a final answer. Instead of jumping directly to a conclusion, the model explicitly works through intermediate steps.

This dramatically improves accuracy on complex tasks requiring logic, math, multi-step reasoning, or decision-making.

---

### **How Chain of Thought Works**

**The Core Mechanism:**

Traditional prompting: Question -> Answer
CoT prompting: Question -> Reasoning Steps -> Answer

By forcing the model to "show its work," you activate deeper reasoning patterns and reduce errors from jumping to conclusions.

**Mental Model:** Think of it like a math teacher requiring students to show their work. The act of writing out steps:

1. Catches logical errors
2. Makes the reasoning auditable
3. Forces systematic thinking instead of pattern matching

---

### **When to Use Chain of Thought**

**Use CoT when:**

- **Complex logic** - Multi-step reasoning, dependencies between facts
- **Math and calculations** - Arithmetic, word problems, financial analysis
- **Decision-making** - Weighing tradeoffs, comparing options
- **Debugging** - Root cause analysis, troubleshooting
- **Planning** - Breaking down complex tasks into steps
- **Verification needed** - You need to audit the reasoning, not just trust the answer

**Don't use CoT when:**

- Simple factual questions (wastes tokens)
- Creative generation (reasoning can stifle creativity)
- Speed is critical (CoT adds latency)
- The task is purely formatting (use Few-Shot instead)

---

### **Chain of Thought vs. Other Techniques**

| Technique            | Output Type             | Best For                   | Token Cost |
| -------------------- | ----------------------- | -------------------------- | ---------- |
| **Zero-Shot**        | Direct answer           | Simple, well-defined tasks | Low        |
| **Few-Shot**         | Pattern matching        | Formatting, classification | Medium     |
| **Chain of Thought** | Reasoning + Answer      | Logic, math, decisions     | Higher     |
| **Tree of Thoughts** | Multiple paths explored | Strategy, ideation         | Highest    |

---

### **The Chain of Thought Template**

```markdown
## SYSTEM
You are an expert {{ROLE}}.
Always think step-by-step before giving the final answer.

## TASK
{{TASK_DESCRIPTION}}

## INPUT
<<<INPUT>>>

## THINKING PROCESS
1. Restate the problem in your own words
2. Identify all constraints and requirements
3. Break down into logical steps
4. Reason through each step explicitly
5. Verify your logic before concluding

## OUTPUT FORMAT
### Step 1: Problem Analysis
[Restate what you're solving]

### Step 2: Constraints
[List all relevant constraints]

### Step 3: Step-by-Step Reasoning
[Work through the logic]

### Step 4: Final Answer
[Your conclusion with justification]
```

---

### **Example 1: Engineering Manager (Build vs. Buy Decision)**

**Use Case:** Deciding whether to build custom authentication or buy a SaaS solution.

```markdown
## SYSTEM
You are a CTO with 15 years experience in B2B SaaS startups.
You excel at build-vs-buy decisions, considering technical debt, team capability, and business constraints.
Think step-by-step through the analysis.

## TASK
Decide whether to build a custom authentication system or buy Auth0/Okta.

## CONTEXT
Current Situation:
- Need: Single Sign-On (SSO) + Multi-Factor Authentication (MFA)
- Team: 3 mid-level engineers, 1 senior engineer
- Timeline: Must launch in 3 months
- Budget: $50k for auth (initial + first year)
- Security: SOC2 compliance required within 6 months

Build Option:
- Use open-source OAuth libraries (Passport.js or similar)
- Estimated: 6 weeks engineering time
- Maintenance: ongoing

Buy Option:
- Auth0: $13k/year for 500 Enterprise connections
- Okta: $15k/year for 500 users
- Integration time: 2-3 days

## THINKING PROCESS
1. Calculate true cost of "build" (including hidden costs)
2. Calculate true cost of "buy" (including integration)
3. Assess team capability and risk
4. Consider timeline and compliance constraints
5. Make recommendation

## OUTPUT FORMAT
### Step 1: Problem Analysis
### Step 2: Build Cost Breakdown
### Step 3: Buy Cost Breakdown
### Step 4: Risk Assessment
### Step 5: Final Recommendation
```

**Expected Output:**

```
### Step 1: Problem Analysis

We need SSO + MFA with SOC2 compliance within 6 months. This is a security-critical system where mistakes have severe consequences (data breaches, compliance failure, customer loss).

Key question: Can we build this faster, cheaper, and more securely than buying a proven solution?

### Step 2: Build Cost Breakdown

Engineering Time:
- Initial build: 6 weeks × 1 senior engineer = 1.5 engineer-months
- At $150k/year salary = $18,750 in labor cost
- Plus 2 weeks for integration/testing = $6,250
- Subtotal: $25,000

Hidden Costs (Critical):
- Security audits for SOC2: External audit required = $15k-$25k
- Ongoing maintenance: 1 day/month × 12 months = 1.5 engineer-months/year = $18,750/year
- Incident response: If auth breaks, entire app is down (high risk)
- Updates: OAuth spec changes, security patches = ongoing burden
- Documentation and knowledge transfer: If senior engineer leaves, we're stuck

First Year Total: $25k (build) + $20k (audit) + $18.75k (maintenance) = $63,750
Ongoing Annual: $18,750 + security updates

### Step 3: Buy Cost Breakdown

Auth0 Enterprise:
- Annual fee: $13,000
- Integration time: 3 days × 1 engineer = $1,875
- No maintenance burden (vendor handles it)
- No security audit needed (Auth0 is SOC2 certified)
- Incident response is vendor's problem
- Instant MFA, SSO, and compliance features

First Year Total: $13k + $1.875k = $14,875
Ongoing Annual: $13,000

Cost Difference: Build costs 4.3x more in year 1, 1.4x more annually.

### Step 4: Risk Assessment

Build Risks:
* HIGH RISK: Security vulnerability. Junior team implementing auth = high chance of mistakes
* HIGH RISK: Timeline. 6 weeks is optimistic. If it slips, launch delay costs $$$$
* MEDIUM RISK: Team bus factor. Only 1 senior engineer knows the system
* HIGH RISK: SOC2 audit failure. Home-built auth will face intense scrutiny
* MEDIUM RISK: Maintenance burden. Takes engineers away from product features

Buy Risks:
* LOW RISK: Vendor lock-in. Auth0/Okta are industry standards, migration path exists
* LOW RISK: Cost increases. Predictable pricing, can negotiate
* VERY LOW RISK: Security. Battle-tested by thousands of companies

### Step 5: Final Recommendation

RECOMMENDATION: Buy Auth0.

Reasoning:
1. Cost: Despite seeming cheaper, build is actually 4x more expensive year 1
2. Risk: Security is NOT a place to cut corners with a junior team
3. Timeline: 3 days integration vs 8 weeks build + testing = 7 weeks saved
4. Compliance: Auth0 is already SOC2 certified = audit becomes trivial
5. Opportunity cost: 1.5 engineer-months can be spent on revenue-generating features

The $13k/year for Auth0 is cheap insurance against:
- Security breaches (avg cost: $4.24M per IBM)
- SOC2 audit failure (delays sales, damages reputation)
- Engineering time spent on undifferentiated heavy lifting

CAVEAT: If we were a 500-person company with dedicated security team, build might make sense. At our stage (small team, tight timeline, compliance pressure), buy is clearly superior.

Action Items:
1. Sign Auth0 Enterprise contract this week
2. Allocate 3 days for senior engineer to integrate
3. Use saved engineer time to ship core product features
```

---

### **Example 2: Marketing Manager (Campaign Diagnostics)**

**Use Case:** Diagnosing why a previously successful campaign suddenly underperforms.

```markdown
## SYSTEM
You are a Performance Marketing Analyst specializing in paid acquisition.
You have deep expertise in Facebook Ads, attribution, and conversion optimization.
Think step-by-step through metric analysis.

## TASK
Diagnose why ROAS (Return on Ad Spend) dropped from 4.0 to 1.5.

## DATA
Time Period: Last 30 days vs Previous 30 days

Previous Period:
- ROAS: 4.0
- Budget: $10,000/month
- Revenue: $40,000
- Audience: Lookalike 1% (warm)
- CPM: $20
- CTR: 2.5%
- Conversion Rate: 3%

Current Period:
- ROAS: 1.5
- Budget: $20,000/month (doubled)
- Revenue: $30,000
- Audience: Broad targeting (cold)
- CPM: $30 (50% increase)
- CTR: 2.5% (stable)
- Conversion Rate: 1.2% (dropped 60%)

Changes Made:
- Doubled budget to "scale"
- Switched from Lookalike to Broad audience
- Same creatives, same landing page

## THINKING PROCESS
1. Analyze the relationship between metrics
2. Identify which metric broke
3. Determine root cause
4. Recommend fix

## OUTPUT FORMAT
### Step 1: Metric Correlation Analysis
### Step 2: Root Cause Identification
### Step 3: Hypothesis Testing
### Step 4: Recommended Fix
```

**Expected Output:**

```
### Step 1: Metric Correlation Analysis

Let me trace the funnel breakdown:

Previous Period Math:
- Impressions: $10k / ($20 CPM / 1000) = 500,000 impressions
- Clicks: 500k × 2.5% CTR = 12,500 clicks
- Click Cost (CPC): $10k / 12.5k clicks = $0.80
- Conversions: 12.5k clicks × 3% CVR = 375 conversions
- Cost Per Acquisition (CPA): $10k / 375 = $26.67
- Average Order Value: $40k / 375 = $106.67
- ROAS: $40k / $10k = 4.0 ✓

Current Period Math:
- Impressions: $20k / ($30 CPM / 1000) = 666,667 impressions
- Clicks: 666k × 2.5% CTR = 16,667 clicks
- Click Cost (CPC): $20k / 16.67k clicks = $1.20 (50% higher)
- Conversions: 16.67k clicks × 1.2% CVR = 200 conversions
- CPA: $20k / 200 = $100 (4x higher!)
- AOV: $30k / 200 = $150 (actually went UP)
- ROAS: $30k / $20k = 1.5 ✗

Key Finding: We got FEWER conversions (200 vs 375) despite spending 2x more.

### Step 2: Root Cause Identification

The funnel breaks at CONVERSION RATE (3% -> 1.2%).

Why NOT the other metrics?
- CPM increase (50%) is expected when switching to Broad (more competition)
- CTR stayed stable (2.5%) = creatives still work
- AOV increased ($107 -> $150) = when people DO convert, they buy more

This tells me:
- The AD is fine (CTR stable)
- The PRODUCT is fine (AOV increased)
- The AUDIENCE is the problem

What changed? Lookalike 1% (warm) -> Broad (cold)

Lookalike audience = people similar to existing customers = high purchase intent
Broad audience = everyone = includes tire-kickers, wrong fit, low intent

Analogy: Previous strategy was fishing in a stocked pond (easy). New strategy is fishing in the ocean (harder).

### Step 3: Hypothesis Testing

Hypothesis: Broad audience has lower purchase intent than Lookalike.

Evidence supporting hypothesis:
1. Conversion rate dropped 60% immediately after audience switch
2. Higher AOV suggests the people who DO convert are still good fits
3. CTR stability means ad creative resonates, but clicks don't convert

Counter-hypothesis: "Maybe the landing page broke?"
- Rejected: If LP broke, AOV wouldn't increase
- Rejected: CTR wouldn't stay stable if messaging misaligned

Counter-hypothesis: "Maybe we exhausted the market?"
- Rejected: We were only spending $10k/month previously, unlikely to saturate
- Rejected: Switching audiences doesn't test this properly

Conclusion: Audience quality is the root cause.

### Step 4: Recommended Fix

IMMEDIATE ACTIONS (This Week):

1. REVERT to Lookalike 1% audience
   - Rationale: Proven 4.0 ROAS, sustainable
   - Expected outcome: ROAS returns to 3.5-4.0 range

2. REDUCE budget back to $10k-$12k/month
   - Rationale: Don't scale what's broken
   - Wait until you fix conversion rate before scaling

SCALING STRATEGY (Next 30 Days):

Don't scale by switching to cold audiences. Instead:

1. Create Lookalike 2% and 3% audiences
   - Slightly broader than 1%, but still warm
   - Test with $2k each to see if ROAS holds

2. Test new creative variations
   - Current creative works for warm audience
   - Cold audience needs different hooks (education vs direct response)

3. Build retargeting funnel
   - Broad clicks that didn't convert = retargeting pool
   - Cheaper to convert warm traffic than find new cold traffic

WRONG WAY TO SCALE:
- ✗ Double budget on cold traffic (what you did)
- ✗ Hope conversion rate improves magically

RIGHT WAY TO SCALE:
- ✓ Find more warm audiences (Lookalike expansion)
- ✓ Improve conversion rate FIRST, then scale
- ✓ Test cold audiences at $1-2k budget, not $20k

Expected Outcome:
- Immediate: ROAS recovers to 3.5-4.0
- 30 days: Lookalike 2-3% tested, find new $5-10k/month in efficient spend
- 60 days: Conversion rate optimization on LP, THEN test cold traffic

Budget Allocation Recommendation:
- $8k: Lookalike 1% (proven performer)
- $2k: Lookalike 2% (test)
- $2k: Lookalike 3% (test)
Total: $12k (vs current $20k wasteful spend)
```

---

### **Example 3: Screenwriter (Plot Consistency Check)**

**Use Case:** Verify timeline consistency in a screenplay.

```markdown
## SYSTEM
You are a Script Supervisor with 20 years experience.
You specialize in continuity and timeline consistency for thrillers and sci-fi.
Think step-by-step through timeline logic.

## TASK
Check if this timeline is logically possible.

## SCENES
Scene 12: INT. LONDON OFFICE - DAY
Sarah receives an urgent call at 9:00 AM London time. She must get to New York for a meeting.

Scene 13: EXT. HEATHROW AIRPORT - DAY  
Sarah rushes through security. Clock shows 10:30 AM.

Scene 14: INT. AIRPLANE - DAY
Sarah on the plane, reading documents.

Scene 15: EXT. NEW YORK OFFICE - DAY
Sarah arrives at the New York office. Clock on wall shows 2:00 PM.

Dialogue: "Made it just in time."

## CONSTRAINTS
- London to New York flight time: ~7-8 hours
- Time zone difference: London is 5 hours ahead of New York (EST)

## THINKING PROCESS
1. Calculate departure/arrival times
2. Check timezone conversions
3. Verify if timeline is physically possible
4. Identify issues if any

## OUTPUT FORMAT
### Step 1: Timeline Breakdown
### Step 2: Flight Logistics
### Step 3: Consistency Check
### Step 4: Verdict + Suggested Fix (if needed)
```

**Expected Output:**

```
### Step 1: Timeline Breakdown

Let me map out the events in both local times and UTC:

Event 1: Phone call in London  
- London time: 9:00 AM  
- UTC: 9:00 AM (London = UTC+0 in winter, UTC+1 in summer)  
- New York time (EST): 4:00 AM (London is 5 hours ahead)

Event 2: At Heathrow  
- London time: 10:30 AM  
- Elapsed since call: 1.5 hours (reasonable for getting to airport)

Event 3: Arrival in New York
- New York time shown: 2:00 PM  
- UTC: 7:00 PM

### Step 2: Flight Logistics

Fastest London -> New York flight:
- Duration: 7-8 hours (best case: 7 hours)
- Typical departure times: Throughout the day
- Typical arrival times: Afternoon/evening NYC time

Let's check if Sarah's journey is possible:

Scenario Analysis:
- She's at Heathrow at 10:30 AM London time
- Earliest possible takeoff: 11:00 AM London (30 min boarding)
- 11:00 AM London = 6:00 AM New York time
- Flight duration: 7 hours (absolute minimum)
- Arrival time: 6:00 AM + 7 hours = 1:00 PM New York time

PROBLEM DETECTED: She arrives in NYC at 2:00 PM according to scene.
Let me verify:
- 11:00 AM London departure
- 7-hour flight
- Arrival: 6:00 PM London time = 1:00 PM NYC time

If she arrives at 2:00 PM NYC, she would need:
- Either an 8-hour flight: 6:00 AM NYC + 8 = 2:00 PM ✓
- Or departed at 12:00 PM London: 7:00 AM NYC + 7 hours = 2:00 PM ✓

### Step 3: Consistency Check

Timeline from CALL to ARRIVAL:
- 9:00 AM call (London)
- 10:30 AM at airport (London)
- Depart ~11:00-11:30 AM (London)
- Arrive 2:00 PM (New York)

Working backwards from 2PM NYC arrival:
- 2:00 PM NYC = 7:00 PM London
- Subtract 7-hour flight = departed 12:00 PM London
- But she was at Heathrow at 10:30 AM London

Time from Heathrow (10:30 AM) to wheels-up (12:00 PM) = 1.5 hours

IS THIS POSSIBLE?
- Security + boarding: 1.5 hours is tight but possible for domestic, nearly impossible for international
- International flights require 2-3 hours before departure
- For a last-minute urgent flight, she'd likely take next available flight

VERDICT: Timeline is BARELY possible but **extremely tight and unrealistic**.

### Step 4: Suggested Fix

OPTION A: Adjust the New York arrival time (Easiest)

Change Scene 15:

EXT. NEW YORK OFFICE - DAY
Sarah arrives, visibly exhausted. Clock shows 3:30 PM.

DIALOGUE: "Cutting it close. Meeting's at 4." s

Timeline:
- 9:00 AM call (London)
- 10:30 AM Heathrow
- 12:30 PM depart London
- 8-hour flight
- 3:30 PM arrive NYC
Total journey: 6.5 hours (realistic)

OPTION B: Add urgency and compress the front (More dramatic)

New Scene 12A: INT. SARAH'S APARTMENT - DAY
Sarah throws clothes in a bag, laptop, passport. Out the door.

Scene 13: EXT. HEATHROW - DAY
Clock shows 9:45 AM (compressed travel time, adds urgency)

Scene 14: INT. SECURITY LINE  
Sarah: "I need to make the 10:30 flight to JFK. Please."
GUARD: "Flight boards in 20 minutes. Run."

Scene 15: INT. AIRPLANE - MOVING
Plane already taxiing. Sarah catches her breath, fastening seatbelt.

Scene 16: EXT. NEW YORK OFFICE - DAY  
Clock: 2:45 PM. Sarah rushes in.

Timeline:
- 9:00 AM call
- 9:45 AM Heathrow (super-rushed)
- 10:30 AM departure (caught it by seconds)
- 7.5 hour flight
- 2:45 PM arrival
Total: 5.75 hours travel time (ultra-tight but possible)

RECOMMENDATION: Use Option A (adjust NYC time to 3:30 PM). Simpler, more realistic, doesn't require adding scenes.
```

---

### **Best Practices for Chain of Thought**

1. **Explicitly Request Step-by-Step**
    - Use phrases: "think step-by-step", "show your work", "reason through this"

2. **Structure the Reasoning**
    - Number the steps
    - Use clear section headers
    - Make it easy to follow the logic

3. **Request Verification**
    - "Double-check your math"
    - "Verify your assumptions"
    - "List what could be wrong with this reasoning"

4. **Combine with Few-Shot for Complex Tasks**
    - Show one example of good reasoning
    - Then ask for CoT on new problem

---

### **Common Mistakes**

**Mistake 1: Not Requesting Explicit Steps**

```
Bad: "What's the answer?"
Good: "Think step-by-step. First restate the problem, then analyze constraints, then solve."
```

**Mistake 2: Accepting First Answer**

```
Bad: LLM gives answer -> you trust it
Good: LLM shows reasoning -> you audit the steps
```

**Mistake 3: Using CoT for Simple Tasks**

```
Bad: "Think step-by-step: What's the capital of France?"
Good: Just ask directly (wastes tokens on trivial questions)
```

---

### **Key Takeaways**

* CoT forces models to show reasoning, dramatically improving accuracy on complex tasks
* Use for logic, math, decisions, debugging—not for simple factual queries
* Structure the output with clear steps makes reasoning auditable
* Higher token cost but worth it for critical decisions
* Combine with other techniques (Few-Shot, Self-Reflection) for best results

---

**Next Chapter Preview:** Chapter 6 covers Tree of Thoughts—exploring multiple reasoning paths and selecting the best one.

## **Chapter 6: Tree of Thoughts (ToT)**

### **What is Tree of Thoughts?**

Tree of Thoughts (ToT) is an advanced prompting technique that explores **multiple reasoning paths** (branches) simultaneously, evaluates each against specific criteria, and selects the optimal solution. Unlike Chain of Thought which follows a linear path, ToT creates a tree structure of possibilities.

This technique excels at strategic decisions, creative ideation, and scenarios where multiple valid approaches exist.

---

### **How Tree of Thoughts Works**

**The Core Mechanism:**

1. **Branch Generation**: Create 3-5 distinct solution approaches
2. **Evaluation**: Analyze each branch against defined criteria (pros/cons, tradeoffs)
3. **Comparison**: Evaluate branches relative to each other
4. **Selection**: Choose the best path with explicit justification

**Mental Model:** Think of it like a chess player considering multiple opening moves. Each move leads to a different game tree. By evaluating branches before committing, you make better strategic choices.

**Key Difference from CoT:**

- CoT: Question -> Step 1 -> Step 2 -> Step 3 -> Answer (linear)
- ToT: Question -> {Branch A, Branch B, Branch C} -> Evaluate -> Best Answer (parallel exploration)

---

### **When to Use Tree of Thoughts**

**Use ToT when:**

- **Multiple valid approaches exist** - No single "correct" answer
- **Strategic decisions** - Hiring, product strategy, market positioning
- **Creative ideation** - Plot development, campaign concepts, design approaches
- **Tradeoff analysis** - Need to explicitly compare options
- **Risk assessment** - Evaluating different risk profiles
- **Exploring solution space** - Don't want to commit to first idea

**Don't use ToT when:**

- There's a clearly optimal solution (use CoT instead)
- Simple binary choices (overkill)
- Speed is critical (ToT is token-intensive)
- You have strong prior data (use that data instead of brainstorming)

---

### **Tree of Thoughts vs. Other Techniques**

| Technique             | Exploration Type          | Best For                      | Complexity |
| --------------------- | ------------------------- | ----------------------------- | ---------- |
| **Zero-Shot**         | Direct answer             | Simple, known tasks           | Low        |
| **Chain of Thought**  | Single path, linear       | Logic, math, debugging        | Medium     |
| **Tree of Thoughts**  | Multiple paths, evaluated | Strategy, ideation, tradeoffs | High       |
| **Graph of Thoughts** | Interconnected network    | Complex system constraints    | Very High  |

---

### **The Tree of Thoughts Template**

```markdown
## SYSTEM
You are an expert {{ROLE}}.
Explore multiple solution approaches, evaluate them systematically, and select the best one.

## TASK
{{TASK_DESCRIPTION}}

## CONTEXT
{{RELEVANT_BACKGROUND}}

## THINKING PROCESS
1. Generate 3-4 distinct solution branches (significantly different approaches)
2. For each branch:
   - Describe the approach
   - List specific advantages
   - List specific disadvantages
   - Assess against evaluation criteria
3. Compare branches directly
4. Select the optimal branch with justification

## EVALUATION CRITERIA
{{CRITERIA_1}}
{{CRITERIA_2}}
{{CRITERIA_3}}

## OUTPUT FORMAT
### Branch A: {{APPROACH_NAME}}
**Description:** ...
**Advantages:** ...
**Disadvantages:** ...
**Criteria Assessment:** ...

### Branch B: {{APPROACH_NAME}}
[Same structure]

### Branch C: {{APPROACH_NAME}}
[Same structure]

### Comparison Matrix
[Direct comparison table]

### Final Decision
**Selected Branch:** ...
**Justification:** ...
```

---

### **Example 1: Engineering Manager (Hiring Strategy)**

**Use Case:** Deciding how to allocate limited headcount budget for a new team.

```markdown
## SYSTEM
You are a VP of Engineering at a Series B startup.
You excel at team composition strategy and hiring decisions.
Explore multiple approaches and select the best one.

## TASK
Decide how to use remaining headcount budget for the AI Platform team.

## CONTEXT
Current Situation:
- Budget: Remaining headcount for 2 junior engineers OR 1 staff engineer OR contractor budget
- Timeline: Must ship MVP in 3 months for investor demo
- Current Team: 3 mid-level generalists (good execution, limited ML expertise)
- Product: Real-time ML inference platform (complex, performance-critical)
- Complexity: Need to handle model serving, scaling, monitoring

Constraints:
- Cannot extend timeline (investor demo is firm commitment)
- Quality matters (performance SLAs committed to customers)
- Post-MVP: Team will own ongoing maintenance

## EVALUATION CRITERIA
1. Speed to MVP (can we ship in 3 months?)
2. Code Quality & Architecture (will it need rewrite after MVP?)
3. Knowledge Retention (what happens after MVP ships?)
4. Risk Level (what are failure modes?)

## THINKING PROCESS
Generate 3-4 hiring approaches, evaluate each, then decide.
```

**Expected Output:**

```
### Branch A: Hire 2 Junior Engineers (Velocity Play)

**Description:**
Bring on two junior engineers (0-2 years experience). Focus on execution speed with close mentorship from existing mid-levels.

**Advantages:**
- Velocity: More hands on keyboard = more features implemented
- Cost-efficient: Junior salaries lower, can hire quickly
- Fresh perspectives: May bring new ideas from recent education
- Parallel work: Can split into two sub-teams for parallel development

**Disadvantages:**
- Mentorship overhead: Mid-levels must spend 30-40% time mentoring
- Architecture risk: Juniors won't catch design flaws early
- Quality variance: Code quality inconsistent, needs heavy review
- ML expertise gap: Team still lacks deep ML/inference knowledge
- Post-MVP burden: Likely need refactor after MVP

**Criteria Assessment:**
- Speed to MVP: 6/10 (more people, but mentorship overhead)
- Code Quality: 4/10 (junior code requires refactoring)
- Knowledge Retention: 7/10 (juniors will grow, but slowly)
- Risk Level: HIGH (architecture mistakes in perf-critical system)

---

### Branch B: Hire 1 Staff Engineer (Expertise Play)

**Description:**
Bring on one staff-level engineer with ML systems experience (8+ years, specialized in model serving/inference).

**Advantages:**
- Architecture: Gets design right from the start
- ML expertise: Deep knowledge of inference optimization, serving patterns
- Mentorship: Uplevels the entire team through code review, pairing
- Quality: High code quality from day one
- Velocity multiplier: Unblocks team 10x faster than they can unblock themselves

**Disadvantages:**
- Hiring time: Staff engineers hard to find (may take 6-8 weeks)
- Single point of failure: If they leave post-MVP, knowledge loss
- Limited capacity: One person can only do so much
- Cost: Higher salary, equity
- Onboarding: Takes 2-3 weeks to be productive (tight timeline)

**Criteria Assessment:**
- Speed to MVP: 7/10 (slower hire, but higher velocity once onboard)
- Code Quality: 9/10 (excellent architecture, minimal tech debt)
- Knowledge Retention: 5/10 (bus factor = 1 person)
- Risk Level: MEDIUM (hiring risk, but technical risk low)

---

### Branch C: Hire 3-Month Contractors (Mercenary Play)

**Description:**
Bring on 2-3 contractors for a 3-month engagement specifically for MVP. No conversion to full-time planned.

**Advantages:**
- Speed: Contractors available immediately (no lengthy hiring)
- Flexible capacity: Can scale up/down based on needs
- Specialized skills: Can hire specific ML inference expertise
- No long-term commitment: Pay only for MVP period
- Parallel execution: Can onboard multiple contractors fast

**Disadvantages:**
- Knowledge loss: All context leaves after 3 months
- Quality risk: Contractors optimize for "done" not "maintainable"
- Handoff burden: Full-time team must learn codebase post-MVP
- Integration friction: Contractors may not align with company practices
- Post-MVP rewrite likely: Built for demo, not production

**Criteria Assessment:**
- Speed to MVP: 9/10 (fastest to ship)
- Code Quality: 3/10 (optimized for demo, not longevity)
- Knowledge Retention: 1/10 (all knowledge walks away)
- Risk Level: HIGH (technical debt bomb, maintenance nightmare)

---

### Branch D: Hybrid - 1 Staff + Delay Non-Critical Features (Quality + Scope Adjustment)

**Description:**
Hire 1 staff engineer AND negotiate with stakeholders to reduce MVP scope by 20-30%, focusing on core demo-worthy features.

**Advantages:**
- Best of both worlds: Expertise + achievable timeline
- Architectural foundation: Staff engineer ensures solid design
- Sustainable: Post-MVP, team can build on solid foundation
- Team growth: Mid-levels learn from staff engineer
- Risk mitigation: Reduces scope = reduces execution risk

**Disadvantages:**
- Stakeholder management: Must convince investors that reduced scope is acceptable
- Perceived compromise: May look like "backing down" on commitments
- Hiring risk: Still need to find staff engineer quickly
- Capacity constraint: One staff + 3 mids may still struggle

**Criteria Assessment:**
- Speed to MVP: 8/10 (reduced scope makes timeline achievable)
- Code Quality: 9/10 (staff engineer ensures quality)
- Knowledge Retention: 8/10 (staff stays, team learns)
- Risk Level: LOW (technical risk low, demo still compelling)

---

### Comparison Matrix

| Criteria | Branch A (2 Juniors) | Branch B (1 Staff) | Branch C (Contractors) | Branch D (Staff + Scope Cut) |
|----------|---------------------|-------------------|----------------------|------------------------------|
| **Speed to MVP** | 6/10 | 7/10 | 9/10 | 8/10 |
| **Code Quality** | 4/10 | 9/10 | 3/10 | 9/10 |
| **Knowledge Retention** | 7/10 | 5/10 | 1/10 | 8/10 |
| **Risk Level** | High | Medium | High | Low |
| **Cost (3 months)** | Low | Medium | Medium | Medium |
| **Post-MVP Burden** | High (refactor) | Low | Very High (rewrite) | Low |

---

### Final Decision

**Selected Branch: D - Hybrid (1 Staff + Scope Reduction)**

**Justification:**

Primary Reasoning:
1. **This is a marathon, not a sprint**: Contractors (Branch C) ship fastest but create 6 months of tech debt cleanup. That's false economy.

2. **Juniors can't handle ML systems complexity** (Branch A): Real-time inference is not a junior-friendly problem. Performance bugs in production are existential risks for ML platforms.

3. **Staff engineer is necessary** (Branch B baseline): But pure Branch B is risky due to capacity. The hybrid approach mitigates this.

4. **Scope negotiation is worth it**: Cutting 20-30% of MVP features to ensure quality foundation is the right tradeoff. A demo that crashes during investor presentation is worse than a smaller demo that works flawlessly.

Specific Action Plan:

1. **This Week**: 
   - Meet with investors/stakeholders
   - Reframe: "We identified the 5 must-have features vs. 3 nice-to-haves. Focusing on must-haves ensures reliable demo and faster iteration post-MVP."
   
2. **Week 2-3**: 
   - Hire staff ML engineer (use specialized recruiter, move fast)
   - Target profile: Someone who's built model serving at scale (Uber ML Platform, Netflix, etc.)

3. **Month 1-3**:
   - Staff engineer focuses on architecture and critical path
   - Mid-levels execute on well-defined tasks with staff review
   - Ship reduced-scope MVP on time

4. **Post-MVP**:
   - Foundation is solid, can iterate quickly
   - Team has learned ML systems patterns from staff engineer
   - Can hire juniors safely after foundation is established

Why Not the Other Branches:

- **Branch A fails** on quality and risk criteria—unacceptable for performance-critical system
- **Branch C fails** on knowledge retention—creates massive post-MVP burden
- **Branch B alone** is close, but capacity risk is too high given timeline

The hybrid approach (Branch D) scores highest on the weighted criteria and provides the best long-term outcome.
```

---

### **Example 2: Marketing Manager (Go-To-Market Strategy)**

**Use Case:** Choosing GTM strategy for a new B2B enterprise product.

```markdown
## SYSTEM
You are a Product Marketing Director with 10 years in B2B SaaS.
You've launched 15+ products, ranging from SMB to Enterprise.
Evaluate multiple GTM strategies and select the best one.

## TASK
Choose the go-to-market strategy for a new Enterprise HR analytics platform.

## CONTEXT
Product: "PeopleInsights" - HR analytics dashboard with predictive turnover modeling
Target Market: Mid-market to Enterprise (500-5000 employees)
Competitive Landscape: Crowded (Workday, BambooHR, Lattice all have analytics)
Differentiation: Our ML models are 30% more accurate at predicting turnover
Pricing: $50k-$200k annual contracts
Sales Cycle: Typically 3-6 months for Enterprise
Budget: $300k for first 6 months of launch

## EVALUATION CRITERIA
1. Customer Acquisition Cost (CAC) efficiency
2. Time to first revenue (urgency: need revenue in 6 months)
3. Brand positioning (want to be seen as premium/enterprise-grade)
4. Scalability (can this GTM approach grow to $10M ARR?)

## THINKING PROCESS
Explore 3 distinct GTM strategies, evaluate, decide.
```

**Expected Output:**

```
### Branch A: Product-Led Growth (PLG) - Self-Serve Free Trial

**Description:**
Launch with generous free trial (30 days, full features). Focus on inbound SEO/content marketing. Let product sell itself.

**Advantages:**
- Low CAC: Organic traffic, minimal sales team needed
- Fast iteration: Direct user feedback via product analytics
- Viral potential: Users share dashboards internally, multi-threading
- Scalable: Can handle 100s of trials simultaneously

**Disadvantages:**
- Enterprise buyers don't self-serve: HR VPs expect demos, not trials
- Long sales cycles despite trial: Still need sales to close $100k deals
- Brand perception risk: "Free trial" = perceived as SMB tool
- Support burden: Trial users need hand-holding for complex HR data integrations

**Criteria Assessment:**
- CAC Efficiency: 8/10 (low cost per trial, BUT low trial-to-paid conversion for Enterprise)
- Time to First Revenue: 4/10 (self-serve buyers are SMB, not big contracts)
- Brand Positioning: 3/10 (free trials position as mid-market, not enterprise)
- Scalability: 9/10 (PLG scales beautifully to SMB/mid-market)

**Verdict**: Wrong market fit. PLG works for $500/mo SaaS, not $100k Enterprise.

---

### Branch B: Sales-Led + Account-Based Marketing (ABM)

**Description:**
Build outbound sales team. Target specific Fortune 1000 HR departments. Personalized campaigns, no free trial, everything is demo + proof-of-concept.

**Advantages:**
- Premium positioning: Outbound sales = enterprise-grade perception
- High ACVs: Sales team can close $100k-$500k deals
- Relationship building: Long sales cycles build customer dependency
- Accurate forecasting: Pipeline visibility with CRM

**Disadvantages:**
- High CAC: Sales team salaries + marketing spend = $150k+ per deal
- Slow ramp: Takes 6 months to build sales team, another 6 to close deals
- Not scalable cheaply: Requires 1 rep per $1M ARR (expensive)
- Competitive: Incumbents (Workday) have entrenched relationships

**Criteria Assessment:**
- CAC Efficiency: 4/10 (very expensive to acquire each customer)
- Time to First Revenue: 5/10 (first deals close in month 9-12, missing 6-month goal)
- Brand Positioning: 9/10 (ABM screams "enterprise")
- Scalability: 6/10 (can scale, but requires constant hiring)

**Verdict**: Right positioning, wrong timing. Can't hit 6-month revenue goal.

---

### Branch C: Event-Led + Thought Leadership

**Description:**
Launch exclusively at HR Tech Conference (Oct). Sponsor keynote, run workshops, position as "the ML-powered future of HR analytics." All marketing budget into one massive event.

**Advantages:**
- Concentrated attention: 10,000 HR decision-makers in one place
- Thought leadership: Position as innovator, not follower
- Press coverage: Major launches at conferences get TechCrunch, etc.
- Lead quality: Conference attendees are active buyers

**Disadvantages:**
- All eggs in one basket: If event flops, 6 months wasted
- Expensive: Sponsorship + booth + travel = $100k-$150k
- Timing risk: Conference is month 5, leaves only 1 month to close deals
- One-time spike: Post-conference, what's the engine?

**Criteria Assessment:**
- CAC Efficiency: 6/10 (cost per lead reasonable IF conference delivers)
- Time to First Revenue: 6/10 (compressed timeline, risky)
- Brand Positioning: 8/10 (big splash positions as major player)
- Scalability: 3/10 (conferences don't repeat monthly)

**Verdict**: High risk, high reward. Not enough diversification.

---

### Branch D: Hybrid - Pilot Program + Sales Team

**Description:**
Offer 3-month pilot programs at 50% discount ($25k). Aggressively sell pilots to 5-10 target accounts. Use pilots as case studies for full sales motion.

**Advantages:**
- Fast revenue: Pilots generate immediate cash flow (month 2-3)
- Risk reduction for buyers: "Try before you buy" for Enterprise
- Case study generation: 3 successful pilots = sales ammunition
- Sales training: Team learns the pitch during pilots
- Conversion path: Pilots convert to full contracts at month 6

**Disadvantages:**
- Discount pressure: Hard to raise price post-pilot
- Pilot support burden: High-touch during pilot period
- Risk of failure: If pilots don't show ROI, hard to sell full contracts
- Limited scale: Can only do 10 pilots max (capacity)

**Criteria Assessment:**
- CAC Efficiency: 7/10 (reasonable cost, pilot fees offset some costs)
- Time to First Revenue: 9/10 (pilots close in 4-6 weeks)
- Brand Positioning: 7/10 (pilots are enterprise-friendly)
- Scalability: 7/10 (pilots convert to accounts, then standard sales)

**Verdict**: Balanced approach. Hits revenue goals while building sales engine.

---

### Comparison Matrix

| Criteria | PLG (A) | ABM (B) | Event (C) | Pilot Program (D) |
|----------|---------|---------|-----------|-------------------|
| **CAC Efficiency** | 8/10 | 4/10 | 6/10 | 7/10 |
| **Time to Revenue** | 4/10 | 5/10 | 6/10 | 9/10 |
| **Brand Positioning** | 3/10 | 9/10 | 8/10 | 7/10 |
| **Scalability** | 9/10 | 6/10 | 3/10 | 7/10 |
| **Total Score** | 24/40 | 24/40 | 23/40 | 30/40 |
| **Risk Level** | Low | Medium | High | Medium-Low |

---

### Final Decision

**Selected Branch: D - Pilot Program + Sales Hybrid**

**Justification:**

Why Branch D Wins:

1. **Solves the timing problem**: PLG (A) and ABM (B) take 9-12 months to revenue. Pilots generate cash in month 2-3, hitting the 6-month goal.

2. **De-risks for Enterprise buyers**: CIOs don't buy $100k software blind. A 3-month pilot at $25k lets them "test drive" with budget already allocated for "HR consulting" (easier approval).

3. **Creates sales assets**: 3-5 successful pilots = case studies, testimonials, reference customers. This accelerates future sales cycles.

4. **Builds repeatable process**: Pilots are a bridge. They train the sales team on objections, use cases, ROI metrics. Post-pilot, we have a proven playbook.

5. **Balances brand + revenue**: Not as premium as pure ABM (Branch B), but way more enterprise-credible than PLG (Branch A).

Execution Plan:

**Months 1-2: Setup**
- Hire 2 sales reps (enterprise SaaS background)
- Create pilot package: $25k for 3 months (normally $50k)
- Build target account list: 50 companies, 500-2000 employees, recent funding

**Months 2-4: Pilot Sales Blitz**
- Outreach to 50 targets, goal: close 10 pilots
- Positioning: "Be among the first 10 companies to use ML-powered turnover prediction"
- Success metric: 5-7 pilots signed

**Months 3-6: Pilot Execution + Conversion**
- White-glove support for pilot customers
- Weekly check-ins, custom reports, executive briefings
- Goal: 60-70% pilot-to-full-contract conversion
- Revenue: 3 pilots convert × $100k = $300k ARR by month 6

**Months 6-12: Scale**
- Use case studies from pilots in marketing
- Transition to standard sales motion (demos, not pilots)
- Expand to ABM for Fortune 500 (Branch B tactics, with proof points from pilots)

Why Not the Others:

- **Branch A (PLG)**: Right for SMB, wrong for Enterprise. Would generate tons of $500/mo customers, not $100k contracts.
- **Branch B (ABM)**: Right long-term, wrong for 6-month goal. This becomes the strategy at month 6+ after pilots prove the market.
- **Branch C (Event)**: Too risky. All budget on one event with no backup plan. Events are great for awareness, bad as sole GTM.

Branch D provides immediate revenue (pilots), builds sales infrastructure (team + process), and creates transition path to scalable ABM motion.
```

---

### **Best Practices for Tree of Thoughts**

1. **Generate Meaningfully Different Branches**
    - Don't create 3 minor variations
    - Each branch should represent a fundamentally different approach

2. **Define Evaluation Criteria Upfront**
    - Prevents post-hoc rationalization
    - Makes comparison objective

3. **Be Honest About Disadvantages**
    - Every approach has tradeoffs
    - Acknowledging cons builds trust in the analysis

4. **Use Comparison Matrices**
    - Visual tables make tradeoffs clear
    - Easier to defend decisions to stakeholders

5. **Justify the Selection**
    - Don't just pick the highest score
    - Explain why that criteria weighting matters in this context

---

### **Common Mistakes**

**Mistake 1: Branches Too Similar**

```
Bad: Branch A (hire in US), Branch B (hire in Canada), Branch C (hire in UK)
Good: Branch A (hire full-time), Branch B (contractors), Branch C (outsource to agency)
```

**Mistake 2: Ignoring Criteria**

```
Bad: Define criteria, then select based on gut feel
Good: Systematically evaluate each branch against each criterion
```

**Mistake 3: No Clear Winner**

```
Bad: "All branches have merit, choose any"
Good: "Branch B scores highest AND aligns with our strategic priorities"
```

---

### **Key Takeaways**

* ToT explores multiple solution paths in parallel, unlike CoT's linear reasoning
* Use for strategic decisions, ideation, and tradeoff analysis
* Define evaluation criteria explicitly before generating branches
* Each branch should be meaningfully different, not minor variations
* Higher token cost but essential for complex decisions with multiple valid approaches
* Comparison matrices make tradeoffs visual and defensible

---

**Next Chapter Preview:** Chapter 7 covers Graph of Thoughts—modeling complex systems with interconnected constraints.

## **Chapter 7: Graph of Thoughts (GoT)**

### **What is Graph of Thoughts?**

Graph of Thoughts (GoT) is the most advanced prompting technique that models reasoning as an **interconnected network of nodes** where constraints and dependencies propagate between elements. Unlike Tree of Thoughts which evaluates independent branches, GoT recognizes that real-world decisions involve **interdependent systems** where changing one element affects others.

This technique excels at complex logistics, system architecture, scheduling with multiple constraints, and optimizing interconnected processes.

---

### **How Graph of Thoughts Works**

**The Core Mechanism:**

1. **Define Nodes**: Identify key components/aspects of the system (people, resources, constraints, goals)
2. **Map Edges**: Define relationships and dependencies between nodes
3. **Constraint Propagation**: Analyze how changing one node affects connected nodes
4. **Optimization**: Find a configuration that satisfies all constraints simultaneously

**Mental Model:** Think of it like solving a Sudoku puzzle. Each cell (node) has constraints, and changing one cell propagates constraints to related cells (edges). The solution must satisfy all constraints at once.

**Key Differences:**

- **CoT**: A -> B -> C -> D (linear chain)
- **ToT**: {Path A, Path B, Path C} (parallel, independent branches)
- **GoT**: Network where A affects B, B affects C, but C also affects A (cyclic dependencies)

---

### **When to Use Graph of Thoughts**

**Use GoT when:**

- **Multiple interdependent constraints** - Changes ripple through the system
- **Resource allocation** - Limited resources shared across multiple needs
- **Scheduling with dependencies** - Tasks have temporal or sequential constraints
- **System architecture** - Components depend on each other
- **Multi-stakeholder decisions** - Optimizing for competing requirements
- **Network optimization** - Traffic flow, supply chain, user journeys

**Don't use GoT when:**

- Constraints are independent (use ToT instead)
- Linear reasoning suffices (use CoT instead)
- System is simple with few dependencies (overkill)
- Speed is critical (GoT is computationally expensive for LLMs)

---

### **Graph of Thoughts vs. Other Techniques**

| Technique             | Structure              | Dependencies                  | Best For                   |
| --------------------- | ---------------------- | ----------------------------- | -------------------------- |
| **Chain of Thought**  | Linear sequence        | Each step depends on previous | Math, logic, sequential    |
| **Tree of Thoughts**  | Parallel branches      | Branches are independent      | Strategy comparison        |
| **Graph of Thoughts** | Interconnected network | Nodes affect each other       | Complex systems, logistics |

---

### **The Graph of Thoughts Template**

```markdown
## SYSTEM
You are an expert {{ROLE}}.
Use Graph of Thoughts to analyze this system with interdependent constraints.

## TASK
{{TASK_DESCRIPTION}}

## NODES (System Components)
Define each node with its:
- Identifier (Node A, B, C, etc.)
- Description
- Independent constraints

## EDGES (Dependencies)
For each relationship, define:
- Connection (A -> B means A affects B)
- Type of dependency
- Constraint propagation rules

## OPTIMIZATION GOAL
{{WHAT_ARE_WE_OPTIMIZING_FOR}}

## PROCESS
1. List all nodes and their individual constraints
2. Map all edges showing how nodes interact
3. Identify conflicts where constraints are incompatible
4. Propose solutions that satisfy maximum constraints
5. Verify that solution doesn't create new conflicts

## OUTPUT FORMAT
### Node Definitions
[List each node with constraints]

### Edge Analysis
[Show how nodes interconnect]

### Conflict Identification
[Which constraints clash?]

### Proposed Solution
[Configuration that optimizes the system]

### Verification
[Check that solution works for all nodes]
```

---

### **Example 1: Engineering Manager (Microservices Migration)**

**Use Case:** Planning migration from monolith to microservices while maintaining system availability.

```markdown
## SYSTEM
You are a Principal Software Architect with 15 years experience.
You specialize in microservices migrations for high-traffic systems.
Use Graph of Thoughts to plan the migration strategy.

## TASK
Plan the migration from a monolithic e-commerce platform to microservices architecture without downtime.

## CONTEXT
Current Monolith Components:
- User authentication
- Product catalog
- Shopping cart
- Payment processing
- Order management
- Inventory tracking

Constraints:
- Zero downtime during migration (24/7 e-commerce site)
- Black Friday in 6 months (cannot migrate during peak)
- Payment processing is PCI-DSS compliant (security critical)
- Shared PostgreSQL database (single point of coupling)
- 100K daily active users

Business Goals:
- Independent scaling (catalog gets 10x more traffic than checkout)
- Faster deployments (currently deploy once/month)
- Team autonomy (3 teams want to own separate services)

## NODES (System Components)

Node A: User Service (Auth + Profile)
- Constraints: Session management, JWT tokens, 24/7 uptime
- Data: Users table (10M rows)

Node B: Catalog Service (Products + Search)
- Constraints: High read traffic (90% of requests), needs caching
- Data: Products table (1M rows), Categories, Images

Node C: Cart Service (Shopping cart)
- Constraints: Must sync with logged-in users AND anonymous users
- Data: Carts table (ephemeral, can lose data with warning)

Node D: Payment Service (Stripe integration)
- Constraints: PCI-DSS compliance, cannot have bugs, zero data loss
- Data: Payment methods (encrypted), Transaction logs

Node E: Orders Service (Order management)
- Constraints: Depends on User, Cart, Payment, Inventory
- Data: Orders table (critical, transactional)

Node F: Inventory Service (Stock tracking)
- Constraints: Must prevent overselling, real-time updates
- Data: Inventory table (updated by Orders AND external warehouse)

Node G: Shared Database (PostgreSQL)
- Constraints: Currently owns ALL data
- Problem: Creates tight coupling

## EDGES (Dependencies)

Edge A -> C: Cart needs User ID for logged-in carts
Edge A -> E: Orders need User info
Edge B -> C: Cart shows product details
Edge C -> E: Checkout converts cart to order
Edge D -> E: Payment confirmation triggers order creation
Edge E -> F: Order creation decrements inventory
Edge F -> B: Catalog shows availability ("In Stock" badge)

Database Edges:
Edge G -> (A, B, C, D, E, F): All services currently read from shared DB

## CONFLICTS

Conflict 1: Database Coupling
- All services share one DB
- Cannot split B (Catalog) if E (Orders) queries Products table directly

Conflict 2: Transactional Consistency
- Order creation spans: Cart + Payment + Inventory + Orders
- Distributed transactions are hard

Conflict 3: Migration Sequencing
- Can't split D (Payment) first - depends on A (Users) and E (Orders)
- Can't split E (Orders) first - depends on A, C, D, F

Conflict 4: Deployment Coordination
- If A (Users) is microservice but E (Orders) is monolith, how do they communicate?

## OPTIMIZATION GOAL
Minimize: Migration risk, downtime, business disruption
Maximize: Team velocity improvement, independent scalability

## PROCESS
Analyze migration order using Graph of Thoughts to avoid breaking dependencies.
```

**Expected Output:**

```
### Node Definitions

Node A: User Service
- Current: Part of monolith, handles auth
- Target: Standalone microservice with own user DB
- Constraints: Must maintain session continuity during migration

Node B: Catalog Service  
- Current: Product listings, search
- Target: Read-heavy microservice, can use cache
- Constraints: High traffic (90% of site), cannot have downtime

Node C: Cart Service
- Current: Shopping cart logic
- Target: Lightweight, stateful microservice
- Constraints: Supports anonymous users (no auth dependency)

Node D: Payment Service
- Current: Stripe API wrapper
- Target: Isolated, PCI-DSS zone
- Constraints: Cannot have bugs, security audited

Node E: Orders Service
- Current: Core transactional logic
- Target: Orchestrates Cart, Payment, Inventory
- Constraints: ACID properties, cannot lose orders

Node F: Inventory Service
- Current: Stock management
- Target: Event-driven, publishes stock updates
- Constraints: Prevent overselling

Node G: Shared Database
- Problem: Single point of coupling
- Solution: Gradually decompose using Strangler Fig pattern

---

### Edge Analysis (Dependencies)

Primary Dependencies:
A (Users) ---reads---> G (DB)
           ---authenticates---> C, E

B (Catalog) ---reads---> G (DB)
            ---displays in---> C

C (Cart) ---reads User---> A
         ---reads Products---> B
         ---creates---> E

D (Payment) ---charges---> Stripe (external)
            ---confirms---> E

E (Orders) ---reads User---> A
           ---consumes Cart---> C  
           ---verifies Payment---> D
           ---decrements---> F

F (Inventory) ---updates---> G (DB)
              ---publishes stock--> B

Critical Path (Transactional):
C (Cart) -> D (Payment) -> E (Order) -> F (Inventory)
   └──────────── Must be atomic ────────────┘

---

### Conflict Identification

**Conflict 1: Chicken-and-Egg Migration**

Problem: Orders (E) depends on Users (A), Cart (C), Payment (D), Inventory (F). Can't migrate E until all dependencies are microservices, but E is core to the monolith.

Impact: If we migrate in wrong order, create distributed monolith.

**Conflict 2: Database Decomposition**

Problem: All nodes query shared DB (G). Splitting DB requires data migration with zero downtime.

Impact: Complex data synchronization during migration.

**Conflict 3: Transactional Guarantees**

Problem: Order creation (E) currently uses DB transactions. In microservices, need distributed transactions or saga pattern.

Impact: Risk of partial failures (payment charged but order not created).

**Conflict 4: Black Friday Constraint**

Problem: Cannot migrate during Q4 (Black Friday, Cyber Monday).

Impact: Only 6 months of non-peak time for migration.

---

### Proposed Solution (Strangler Fig Migration)

**Phase 1 (Months 1-2): Extract Read-Only Services**

Migrate: B (Catalog)

Why First:
- Read-only (no writes to DB)
- High traffic (proves scaling works)
- Few dependencies (only reads Products table)
- Failure mode is safe (fall back to monolith)

Implementation:
1. Create Catalog microservice
2. Replicate Products table to Catalog DB (read replica)
3. Route 10% of traffic to microservice (canary)
4. Monitor for 2 weeks
5. Route 100% of traffic
6. Monolith still owns Products table (writes)

Validation: Catalog scales independently, page load time improves.

---

**Phase 2 (Months 2-3): Extract Stateless Services** 

Migrate: C (Cart)

Why Second:
- Stateful but ephemeral (can lose carts with warning)
- Low risk (users rebuilding cart is annoying but not catastrophic)
- Reduces load on monolith

Implementation:
1. Create Cart microservice with Redis (not DB)
2. API Gateway routes `/cart/*` to microservice
3. Cart calls User Service (A, still monolith) for auth via API
4. If Cart service fails, show banner: "Cart temporarily unavailable"

Edge Handling:
- Cart -> User: API call to monolith User endpoints
- Cart -> Products: Read from Catalog microservice (Phase 1)

---

**Phase 3 (Months 3-4): Extract Critical Write Services**

Migrate: F (Inventory)

Why Third:
- Isolated write domain (only Inventory updates stock)
- Publishes events (shows event-driven pattern)
- Reduces contention on main DB

Implementation:
1. Create Inventory microservice with own DB
2. Sync inventory data (one-time migration)
3. Inventory publishes "StockUpdated" events
4. Catalog subscribes to events, updates cache
5. Monolith Orders (E) still calls Inventory API for decrements

Event Flow:

Order Created -> Inventory.decrementStock(productId, qty)
              -> Inventory emits "StockUpdated" event
              -> Catalog invalidates cache


Testing: Place test orders, verify inventory decrements, catalog updates.

---

**Phase 4 (Month 5, Pre-Black Friday Freeze): Extract Auth**

Migrate: A (Users)

Why Fourth:
- Now multiple services need auth (Cart, future Orders)
- Centralized auth service enables SSO
- Must be done before migrating Orders (E)

Implementation:
1. Extract User microservice
2. Use database-per-service: Replicate Users table to User Service DB
3. Implement JWT token issuance
4. All services validate JWT (shared secret or public key)
5. Monolith calls User Service API for user lookups

Critical Period: This is month 5. Must be stable before Black Friday freeze (month 6).

FREEZE WINDOW: Month 6 (Nov). NO CHANGES.

---

**Phase 5 (Months 7-8, Post-Black Friday): Extract Payments**

Migrate: D (Payment)

Why After Black Friday:
- Critical path for revenue
- PCI-DSS compliance requires audit
- Cannot risk during peak

Implementation:
1. Create Payment microservice (isolated, security hardened)
2. Encrypt all payment data at rest
3. Payment service is the ONLY service that talks to Stripe
4. Pass PCI-DSS audit for Payment service boundary
5. Orders calls Payment API

Security: Payment service in separate VPC, restricted access.

---

**Phase 6 (Months 9-11): Extract Orders**

Migrate: E (Orders)

Why Last:
- Most complex (orchestrates everything)
- All dependencies are now microservices
- Can use saga pattern for distributed transactions

Implementation:
1. Orders microservice with own DB
2. Order creation saga:
   - Create pending order
   - Call Payment -> if fails, cancel order
   - Call Inventory.decrement -> if fails, refund payment
   - Mark order confirmed -> publish "OrderCreated" event
3. Compensating transactions for failures

Saga Flow:

1. POST /orders -> OrderService
2. OrderService -> PaymentService.charge()
3. If success -> InventoryService.decrement()
4. If success -> OrderService.confirm()
5. If any failure -> compensate (refund, re-add stock)


Testing: Chaos engineering - kill services mid-transaction, verify rollback.

---

**Phase 7 (Month 12): Decommission Monolith**

Final Steps:
1. All traffic routed to microservices
2. Monolith runs in read-only mode for 1 month (safety net)
3. Shut down monolith
4. Archive code

---

### Verification (Constraint Satisfaction)

Check each original constraint:

**Zero Downtime:**
- Achieved via Strangler Fig (both monolith and microservices run in parallel)
- Each phase validates before full cutover

**Black Friday Safety:**
- Migration freeze in Month 6 (November)
- High-risk services (Payment, Orders) migrated after Q4

**Independent Scaling:**
- Catalog can scale to 100 instances during traffic spikes
- Orders scales independently to handle checkout burst

**Team Autonomy:**
- 3 teams each own microservices
- Deploy independently (no coordination needed)

**Data Integrity:**
- Saga pattern ensures transactional consistency
- Compensating transactions handle failures

**PCI-DSS Compliance:**
- Payment service isolated and audited
- Reduced compliance scope (only Payment service, not entire system)

---

### Edge Case Handling

**What if Catalog microservice fails in Phase 1?**
- Fallback: API Gateway routes traffic back to monolith
- Impact: None (users don't notice)

**What if we discover bug in Orders saga post-migration?**
- Mitigation: Feature flag to route Orders back to monolith
- Recovery: 1-hour RTO

**What if Black Friday traffic 10x higher than expected?**
- Autoscaling configured for each microservice
- Catalog, Auth can scale horizontally without limit

---

### Migration Gantt Chart


Month 1-2:  [Catalog Migration]
Month 2-3:  [Cart Migration]
Month 3-4:  [Inventory Migration]
Month 5:    [User Migration] <- Deadline before freeze
Month 6:    [BLACK FRIDAY FREEZE - NO CHANGES]
Month 7-8:  [Payment Migration]
Month 9-11: [Orders Migration + Saga implementation]
Month 12:   [Monolith Decommission]

---

### Final Architecture (Post-Migration)

                    [API Gateway]
                          |
      ┌──────────────┬────┴────┬────────────────┬─────────────┐
      |              |         |                |             |
  [Catalog]      [Cart]   [User Auth]     [Payment]     [Orders]
      |              |         |                |             |
      └──[events]────┴─────────┴──[API calls]───┴─────────────┘
                              |
                         [Inventory]


All services:
- Independent databases
- Independent scaling
- Independent deployments
- Event-driven communication where async
- API calls where synchronous needed
```

---

### **Example 2: Production Manager (Film Shoot Scheduling)**

**Use Case:** Scheduling a complex shoot day with overlapping constraints.

```markdown
## SYSTEM
You are a Unit Production Manager for a feature film.
You excel at logistics and scheduling with hard constraints.
Use Graph of Thoughts to create the shoot schedule.

## TASK
Plan the shooting schedule for a beach wedding scene with multiple constraints.

## CONTEXT
Scene Requirements:
- Location: Public beach (requires permits)
- Actors: Bride (adult), Groom (adult), Ring Bearer (child, age 7)
- Crew: 30 people
- Equipment: Camera, lighting, sound, drone for aerials
- Duration: Estimated 8 hours of shooting

## NODES (Constraints)

Node A: Golden Hour Lighting
- Description: Director wants "magic hour" light (soft, golden)
- Constraint: Only available 5:00 PM - 6:00 PM
- Non-negotiable: Director's artistic vision

Node B: Child Actor (Ring Bearer)
- Description: 7-year-old boy, plays ring bearer
- Legal Constraint: California law - child can work max 4 hours/day
- Available: 1:00 PM - 5:30 PM (including breaks)
- Must leave by 5:30 PM (parent pickup)

Node C: Tide Schedule
- Description: Beach location depends on tide
- Constraint: High tide at 5:15 PM covers the beach
- Usable beach: Low tide (12:00 PM - 4:00 PM)
- At 5:15 PM: Beach is underwater

Node D: Permits
- Description: City beach permit
- Allowed hours: 10:00 AM - 6:00 PM
- Restriction: No filming after 6:00 PM (noise ordinance)

Node E: Drone Shots
- Description: Aerial establishing shots
- Constraint: FAA rules - no drone after sunset (6:30 PM in summer)
- Weather: Winds pick up after 4:00 PM (makes drone unstable)
- Optimal: 10:00 AM - 3:00 PM (calm winds)

Node F: Lead Actors
- Description: Bride and Groom availability
- Available: Full day (10:00 AM - 6:00 PM)
- Preference: Not too early (makeup takes 2 hours)

## EDGES (Dependencies)

Edge A ∩ B: Conflict
- Golden Hour (5-6 PM) vs Child must leave by 5:30 PM
- Overlap: Only 5:00-5:30 PM (30 minutes)

Edge A ∩ C: Conflict  
- Golden Hour (5-6 PM) vs Beach underwater at 5:15 PM
- Impossible: Cannot shoot on beach during golden hour

Edge B ∩ C: Compatible
- Child available 1-5:30 PM vs Beach usable 12-4 PM
- Overlap: 1:00-4:00 PM (3 hours)

Edge E ∩ A: Conflict
- Drone needs calm winds (10 AM-3 PM) vs Golden Hour (5-6 PM)
- Must choose: Either drone OR golden hour ground shots

Edge B (child scenes) requires F (lead actors)
- Child scenes must be shot when both are present

## CONFLICTS

Primary Conflict: Golden Hour Impossibility
- Director wants Golden Hour (5-6 PM)
- Beach is underwater at 5:15 PM
- Child must leave at 5:30 PM
- CANNOT SATISFY ALL THREE

Secondary Conflict: Drone Timing
- Drone needs morning (calm winds)
- Golden hour is evening
- Cannot have both in same location

## OPTIMIZATION GOAL
Maximize: Director's vision, actor availability, shot quality
Constraints: Legal (child labor), Physical (tide), Regulatory (permits)

## PROCESS
Propose solutions that resolve conflicts via creative workarounds.
```

**Expected Output:**

```
### Node Analysis

Node A: Golden Hour (5-6 PM) - IMPOSSIBLE DUE TO TIDE
Node B: Child (1-5:30 PM) - HARD CONSTRAINT (legal)
Node C: Tide (Beach gone at 5:15 PM) - HARD CONSTRAINT (physics)
Node D: Permits (10 AM-6 PM) - HARD CONSTRAINT (legal)
Node E: Drone (Best: 10 AM-3 PM) - SOFT CONSTRAINT (quality)
Node F: Leads (10 AM-6 PM) - FLEXIBLE

---

### Edge Conflict Map


Golden Hour (A) 
    |
    X------- Beach Underwater (C)  <- IMPOSSIBLE
    |
    X------- Child Ends 5:30 PM (B) <- TIGHT (only 30min overlap)

Child (B)
    |
    ✓------- Beach (C) [1-4 PM overlap] <- WORKABLE
    |
    ✓------- Leads (F) [full overlap] <- NO ISSUE

Drone (E)
    |
    X------- Golden Hour (A) <- TIMING CONFLICT

---

### Conflict Resolution Options

**Option 1: Abandon Golden Hour Beach Shot**
- Accept that beach + golden hour is physically impossible
- Shoot beach scenes during optimal tide (12-4 PM)
- Get golden hour elsewhere (different location or green screen)

**Option 2: Green Screen Golden Hour**
- Shoot beach scenes 12-4 PM (mid-day light)
- Shoot actors against green screen 5-6 PM (golden hour light)
- Composite in post-production

**Option 3: Morning "Magic Hour"**
- Use morning golden hour instead (6-7 AM)
- Problem: Beach is public, may have tourists/joggers
- Problem: Crew call time 4 AM (expensive, crew fatigue)

**Option 4: VFX + Partial Shoot**
- Shoot establishing drone shots at low tide (12-3 PM)
- Shoot close-ups of actors at golden hour (5-5:30 PM) on studio beach set
- VFX combine the two

---

### Proposed Solution: Hybrid Schedule

**DECISION: Option 4 (Hybrid Real + Studio)**

Rationale:
- Preserves director's golden hour vision
- Respects child labor laws
- Works within tide constraints
- Minimizes VFX cost (only backgrounds, not actors)

Implementation:

**Morning Shoot (10:00 AM - 12:00 PM): Drone Aerials**

Location: Beach (Low Tide)
- 10:00 AM: Crew call, setup drone
- 10:30 AM - 12:00 PM: Capture all aerial establishing shots
- Why now: Calm winds, good light, low tide exposes full beach
- Actors: NOT NEEDED (aerials are wide shots, use stand-ins)

**Afternoon Shoot (1:00 PM - 4:00 PM): Beach Ground Shots**

Location: Beach (Low Tide)
- 1:00 PM: Lead actors + child arrive (makeup complete)
- 1:30 PM - 4:00 PM: Shoot all beach scenes with cast
  - Wide shots of wedding ceremony
  - Ring bearer walking down aisle
  - Bride/groom vows
- Child actor hours: 1:30-4:00 PM (2.5 hours, within 4-hour limit)
- 4:00 PM: Tide starts coming in, wrap beach location

**Evening Shoot (5:00 PM - 6:00 PM): Studio Golden Hour Close-Ups**

Location: Studio beach set (sand, backdrop)
- 5:00 PM: Move to studio stage (10 min drive from beach)
- 5:10 PM - 6:00 PM: Golden hour close-ups
  - Bride/groom portraits in golden light
  - Romantic close-ups, vows, ring exchange
  - NO child actor (already wrapped for the day)
- Backdrop: Green screen OR studio beach set with controlled lighting mimicking golden hour

**Post-Production:**
- VFX composites: Aerial drone footage (morning) + Beach ceremony (afternoon) + Close-ups (golden hour studio)
- Result: Looks like one continuous golden hour beach wedding

---

### Schedule Gantt Chart

10:00 ─┬─ [Drone Setup]
       |
11:00 ─┼─ [Drone Aerials] <- No actors, calm winds
       |
12:00 ─┼─ [Crew Lunch Break]
       |
13:00 ─┼─ [Cast Arrives]
       |
14:00 ─┼─ [Beach Ground Shots] <- All actors, low tide
       |               Child: 1:30-4:00 PM ───┐
15:00 ─┼─             |                       |
       |               ├ Lead Actors: 1:30-6:00 PM
16:00 ─┼─ [Tide In]   | (continue to studio) |
       |               |                       |
17:00 ─┼─ [Studio Golden Hour Close-ups] <────┘
       |
18:00 ─┴─ [Wrap]

---

### Verification (Constraint Satisfaction)

**Node A (Golden Hour):** 
- Satisfied via studio with controlled lighting (5-6 PM)
- Director gets golden hour look on close-ups

**Node B (Child Actor):**
- Worked 1:30-4:00 PM (2.5 hours) ✓
- Left before 5:30 PM (wrapped at 4:00 PM) ✓
- Within 4-hour legal limit ✓

**Node C (Tide):**
- Beach scenes shot 1:30-4:00 PM (low tide) ✓
- Wrapped before tide covers beach (4:00 PM < 5:15 PM) ✓

**Node D (Permits):**
- All beach filming 10 AM-4 PM (within 10 AM-6 PM permit) ✓
- Studio has no permit restrictions ✓

**Node E (Drone):**
- Drone flown 10:30 AM-12 PM (optimal calm winds) ✓
- Before wind picks up (4 PM) ✓

**Node F (Lead Actors):**
- Available full day, used 1:30-6:00 PM ✓
- Makeup done off-clock (before 1:00 PM) ✓

---

### Risk Mitigation

**Risk: Bad weather on shoot day**
- Mitigation: Have backup date (permits allow 2 dates)
- Weather window: Check 5-day forecast, reschedule if storms

**Risk: Drone malfunction**
- Mitigation: Rent backup drone, have pilot on standby
- Alternative: Use helicopter for aerials (more expensive)

**Risk: Child gets tired/uncooperative**
- Mitigation: Shoot child scenes FIRST (1:30-2:30 PM when fresh)
- Have child wrangler + toys for breaks

**Risk: Studio looks fake vs real beach**
- Mitigation: Production designer matches sand color, lighting to beach
- VFX blends edges so transition is seamless

---

### Budget Impact

Costs:
- Drone rental + pilot: $2,000
- Studio rental (4 hours): $1,500
- VFX compositing (3 shots): $5,000
- Backup weather day insurance: $3,000

Total: $11,500

Alternative (try to shoot during golden hour on beach):
- Would require TIME MACHINE to change tide schedule
- Cost: IMPOSSIBLE

Conclusion: $11,500 is cheap to solve an unsolvable physics problem.
```

---

### **Best Practices for Graph of Thoughts**

1. **Explicitly Map All Dependencies**
    - Draw the graph on paper first
    - Identify ALL edges, not just obvious ones

2. **Distinguish Hard vs Soft Constraints**
    - Hard: Legal, physical laws (cannot violate)
    - Soft: Preferences, quality (can compromise)

3. **Look for Constraint Propagation**
    - Changing Node A affects B, which affects C
    - Trace ripple effects through the graph

4. **Identify Cyclic Dependencies**
    - A depends on B, B depends on C, C depends on A = deadlock
    - Break cycles with creative solutions

5. **Optimize for Critical Path**
    - Which nodes are on the critical path?
    - Focus optimization efforts there

---

### **Common Mistakes**

**Mistake 1: Treating Graph as Tree**

```
Bad: Evaluate branches independently (ignores dependencies)
Good: Recognize that changing one node affects connected nodes
```

**Mistake 2: Ignoring Cyclic Dependencies**

```
Bad: "We'll migrate User Service first, then Orders"
Reality: Orders depends on Users, but Users also queries Orders (recent purchases)
Good: Identify the cycle, break it with event-driven patterns
```

**Mistake 3: Over-Optimizing Soft Constraints**

```
Bad: Spend 3 hours optimizing actor preference (soft)
Good: Satisfy hard constraints (legal, physics) first, then optimize soft
```

---

### **Key Takeaways**

* GoT models systems as interconnected networks where constraints propagate
* Use for logistics, architecture, scheduling with dependencies
* Map ALL nodes and edges explicitly before proposing solutions
* Distinguish hard constraints (cannot violate) from soft (can compromise)
* Verify that proposed solution satisfies constraints across the entire graph
* Most computationally expensive prompting technique, but necessary for complex systems

---

**Next Chapter Preview:** Chapter 8 covers Self-Reflection—the iterate and improve loop for quality control.

## **Chapter 8: Self-Reflection (Reflexion)**

### **What is Self-Reflection?**

Self-Reflection (also called Reflexion) is a prompting technique that implements an iterative improve loop: **Draft -> Critique -> Refine**. Instead of accepting the LLM's first output, you explicitly instruct it to self-critique against specific quality criteria, then produce an improved version.

This technique dramatically improves output quality for sensitive communications, creative work, and any task where excellence > speed.

---

### **How Self-Reflection Works**

**The Core Mechanism:**

1. **Draft**: Generate an initial version without overthinking
2. **Critique**: Evaluate the draft against explicit quality criteria (checklist)
3. **Refine**: Produce a polished version that addresses the critique

**Mental Model:** Think of it like pair programming with yourself. The "draft mode" focuses on getting ideas out. The "critique mode" acts as code reviewer. The "refine mode" implements the feedback.

**Key Insight:** By separating generation from evaluation, you prevent the LLM from self-censoring during creation. The critique step provides structure feedback, leading to higher quality output.

---

### **When to Use Self-Reflection**

**Use Self-Reflection when:**

- **Quality is critical** - Performance reviews, public statements, legal documents
- **Sensitivity matters** - Crisis communications, difficult conversations, apologies
- **Creative polish needed** - Dialogue, marketing copy, storytelling
- **Multiple constraints** - Output must satisfy several competing requirements
- **Learning from mistakes** - You want to see what was wrong with the first draft

**Don't use Self-Reflection when:**

- First draft is good enough (faster prompts available)
- Speed > quality (e.g., internal brainstorming)
- Task is simple and objective (e.g., data extraction)
- You're already iterating manually (don't double the work)

---

### **Self-Reflection vs. Other Techniques**

| Technique            | Iterations | Quality Control     | Best For                |
| -------------------- | ---------- | ------------------- | ----------------------- |
| **Zero-Shot**        | 1 pass     | None                | Simple, known tasks     |
| **Few-Shot**         | 1 pass     | Learn from examples | Formatting, patterns    |
| **Chain of Thought** | 1 pass     | Show reasoning      | Logic, math             |
| **Self-Reflection**  | 2-3 passes | Explicit critique   | Quality-critical output |

---

### **The Self-Reflection Template**

```markdown
## SYSTEM
You are an expert {{ROLE}}.
You will draft, critique, and refine your output to ensure excellence.

## TASK
{{TASK_DESCRIPTION}}

## QUALITY CRITERIA (Critique Checklist)
Your output must satisfy ALL of these criteria:
1. {{CRITERION_1}}
2. {{CRITERION_2}}
3. {{CRITERION_3}}
4. {{CRITERION_4}}

## PROCESS
Step 1: Draft
- Write an initial version focusing on content, not perfection

Step 2: Critique
- Evaluate your draft against each quality criterion
- For each criterion, ask: "Does this draft satisfy it? Why or why not?"
- Identify specific weaknesses with line-level detail

Step 3: Refine
- Rewrite addressing every critique point
- Verify the refined version solves the identified problems

## OUTPUT FORMAT
### Draft Version
[Initial attempt]

### Critique
**Criterion 1 ({{NAME}}):** [Assessment + specific issues]
**Criterion 2 ({{NAME}}):** [Assessment + specific issues]
...

### Refined Version
[Polished final version]
```

---

### **Example 1: Engineering Manager (Performance Review)**

**Use Case:** Writing constructive feedback for a talented but difficult engineer.

```markdown
## SYSTEM
You are a Director of Engineering with 12 years of management experience.
You specialize in delivering difficult feedback that motivates rather than demoralizes.
Use the Draft-Critique-Refine process.

## TASK
Write a performance review for Sarah, a Senior Engineer.

## CONTEXT
Sarah's Situation:
- Technical skills: Top 5% of the team (excellent code quality, fast delivery)
- Problem: Toxic in code reviews (dismissive comments, makes juniors feel stupid)
- Specific incident: Last week, commented "This is amateur hour" on a junior's PR
- Impact: Two junior engineers mentioned Sarah in exit interviews as reason for leaving
- Company value: "Respect and collaboration"

Goal: Get Sarah to change behavior without losing her (hard to replace senior talent)

## QUALITY CRITERIA (Critique Checklist)

1. **Actionable**: Feedback must include specific behaviors to change, not vague adjectives
2. **Balanced**: Must acknowledge strengths before addressing weaknesses (ratio: 2 positives to 1 negative)
3. **Objective**: Use SBI model (Situation-Behavior-Impact), not subjective labels like "rude"
4. **Growth-Oriented**: Focus on future improvement, not punishment for past actions
5. **Aligned to Company Values**: Reference company values explicitly
6. **Non-Defensive**: Tone should make Sarah want to improve, not argue/quit

## PROCESS
Draft -> Critique -> Refine
```

**Expected Output:**

```
### Draft Version

PERFORMANCE REVIEW - SARAH CHEN
Q4 2024

Technical Performance: Excellent
Sarah continues to be one of our strongest technical contributors. Code quality is consistently high, and delivery velocity is top-tier.

Collaboration: Needs Improvement
Sarah has been rude in code reviews. Multiple team members have complained about her dismissive attitude. She needs to be more respectful and collaborative. This behavior violates our company values and must change immediately.

Recommendation: Performance Improvement Plan

---

### Critique

**Criterion 1 (Actionable):** FAILS
- "Be more respectful" is vague. What does that mean in practice?
- No specific behaviors to change
- No concrete actions Sarah can take tomorrow

**Criterion 2 (Balanced):** PARTIAL PASS
- Acknowledges technical strength
- But spends more words on criticism than praise (poor ratio)
- Ends on negative note ("must change immediately") which feels punitive

**Criterion 3 (Objective):** FAILS
- "Rude" is subjective - what does that mean?
- "Dismissive attitude" is interpretation, not behavior
- No specific examples with SBI (Situation-Behavior-Impact) model
- Sarah can argue: "I wasn't rude, I was just direct"

**Criterion 4 (Growth-Oriented):** FAILS  
- "Must change immediately" sounds like threat
- "Performance Improvement Plan" implies punishment
- No partnership language ("we" vs "you must")
- Focuses on past problems, not future solutions

**Criterion 5 (Aligned to Values):** PARTIAL PASS
- Mentions company values
- But doesn't explain how Sarah's behavior conflicts with them

**Criterion 6 (Non-Defensive):** FAILS
- Accusatory tone ("you have been rude")
- Multiple team members complained" makes Sarah feel ganged-up on
- Ends with threat (PIP)
- High likelihood Sarah quits or argues

Overall Assessment: This draft would likely backfire. Sarah would either:
A) Quit (we lose senior engineer)
B) Become defensive and not change
C) File HR complaint about unfair review

---

### Refined Version

PERFORMANCE REVIEW - SARAH CHEN
Senior Software Engineer | Q4 2024

**Executive Summary**

Sarah remains one of our most valuable technical contributors. Her code quality, system design skills, and delivery velocity are consistently in the top 5% of the engineering team. This review focuses on an opportunity to amplify Sarah's impact by refining her collaboration approach, particularly in code reviews.

---

**Technical Excellence (Exceeds Expectations)**

Strengths:
- Delivered 3 major features this quarter with zero post-release bugs
- Architectural design for the payments refactor was exemplary - reduced latency by 40%
- Consistently provides thorough, thoughtful code reviews that catch critical issues
- Deep expertise in distributed systems is becoming a team asset

Specific Example:
In October, Sarah identified a race condition in the checkout flow that would have caused data corruption in production. Her technical rigor saved us from a potential P0 incident.

Impact: Sarah's technical bar raises the quality of the entire team's output.

---

**Collaboration & Leadership (Meets Expectations with Growth Area)**

Strengths:
- Willing to jump in and help when teammates are blocked
- Shares knowledge through architecture docs and tech talks
- Mentored Alex (Mid-level) on distributed systems patterns

Growth Opportunity:
Sarah's direct communication style, while effective for technical discussions, sometimes lands differently in code review contexts. Our company value of "Respect and Collaboration" means creating an environment where all engineers, especially junior ones, feel safe to learn and grow.

**Specific Situation (SBI Model):**

Situation: PR #1247 from Jamie (Junior Engineer), week of Nov 12
Behavior: Comment left: "This is amateur hour. Did you even test this?"
Impact: 
- Jamie felt discouraged and mentioned this in our 1:1 as a reason they're considering leaving
- Two other engineers saw the comment and now hesitate to ask Sarah for reviews
- Creates perception that Sarah values being right over helping others grow

**Why This Matters:**

Technical excellence loses leverage if knowledge doesn't multiply across the team. When junior engineers avoid asking Sarah for reviews (our best reviewer), they ship lower-quality code. The team's overall output suffers.

---

**Development Plan (Partnership Approach)**

Goal: Help Sarah translate her exceptional technical standards into mentorship that uplifts the team.

**Concrete Actions:**

1. **Code Review Communication (Starting Dec 1)**
   - Before posting critique, ask: "How would I want to receive this feedback?"
   - Use the "Compliment Sandwich": 1 specific thing done well + critique + 1 growth suggestion
   - Example revision of above comment:
     - Old: "This is amateur hour"
     - New: "Good start on the error handling. The test coverage is missing edge cases - specifically, what happens if the API returns 429? Let's add tests for rate limiting scenarios."

2. **Monthly Mentorship (Ongoing)**
   - Pair with one junior engineer per month on PRs before they submit
   - Goal: Catch issues in pairing session, not in public PR comments
   - This builds juniors up AND reduces Sarah's review burden

3. **Feedback Loop (Weekly check-ins for 6 weeks)**
   - Manager will share anonymized feedback on code review tone
   - We'll track: Are juniors submitting more PRs to Sarah? (Success metric)
   - Adjust approach based on what's working

---

**Why I'm Confident Sarah Will Excel:**

Sarah already demonstrates the technical rigor this requires. The same attention to detail that makes her code excellent can make her mentorship exceptional. This is a skill upgrade, not a personality change.

Many senior engineers go through this transition. The best companies invest in helping technical leaders become people leaders.

---

**Next Steps:**

1. This week: Sarah and I will co-draft a code review template together
2. Dec 1: Begin using new communication approach
3. Mid-Dec: Check-in meeting to assess progress
4. End of Q1: Reassess in next performance review

I'm excited to see Sarah's leadership expand to match her technical abilities.

---

**Overall Rating: Exceeds Expectations**
(Technical excellence is undeniable; collaboration improvement in progress)

**Recommendation: Promotion to Staff Engineer track** (contingent on demonstrated mentorship growth in Q1)
```

---

### **Example 2: Marketing Manager (Crisis Communications)**

**Use Case:** Writing a public apology for a Black Friday service outage.

```markdown
## SYSTEM
You are a crisis communications expert specializing in tech company PR.
You understand that apologizing poorly makes things worse.
Use Draft-Critique-Refine to nail this.

## TASK
Write a Twitter thread (3-4 tweets) apologizing for a 4-hour outage on Black Friday.

## CONTEXT
What Happened:
- E-commerce site went down 10 AM - 2 PM EST on Black Friday
- Peak shopping hours (cost: ~$2M in lost revenue)
- Cause: Database migration script had a bug, caused cascading failures
- Customer impact: 50,000 shoppers couldn't checkout, lost carts
- Social media: Customers are ANGRY, trending #BlackFridayFail

Current Situation:
- Site is back up
- Engineering team identified root cause
- Customers want answers AND compensation

Constraints:
- Cannot blame individuals (no "our engineer made a mistake")
- Must be authentic, not corporate-speak
- Need to offer something concrete (not just "sorry")

## QUALITY CRITERIA

1. **Empathy**: Acknowledge customer frustration and lost time
2. **Transparency**: Explain what happened (technical but understandable)
3. **Accountability**: Take ownership, no excuses or deflection
4. **Action**: Concrete next steps AND compensation
5. **Brevity**: Twitter format, easily shareable
6. **Tone**: Professional but human, not robotic corporate

## PROCESS
Draft -> Critique -> Refine
```

**Expected Output:**

```
### Draft Version

**Tweet 1:**
Our servers experienced an outage today from 10am-2pm EST. We sincerely apologize for any inconvenience this may have caused.

**Tweet 2:**
We are working to ensure this doesn't happen again. Thank you for your patience and understanding.

**Tweet 3:**
If you experienced issues, please contact support@company.com

---

### Critique

**Criterion 1 (Empathy):** FAILS
- "Inconvenience" minimizes impact - people lost hours of shopping and deals
- "May have caused" implies some people weren't affected (everyone was)
- No acknowledgment of emotional impact (frustration, disappointment)
- Tone is detached, corporate

**Criterion 2 (Transparency):** FAILS
- "Servers experienced an outage" is passive voice (servers didn't experience anything, WE broke them)
- Zero explanation of what actually happened
- Customers left guessing: Was it a hack? Bad code? Incompetence?

**Criterion 3 (Accountability):** FAILS
- Passive voice avoids responsibility
- "Working to ensure" is future-looking, doesn't own the present failure
- No apology from a named person (CEO, CTO)

**Criterion 4 (Action):** FAILS
- No compensation offered
- "Contact support" puts burden on customers
- "Working to ensure" is vague - what specific changes?

**Criterion 5 (Brevity):** PASSES
- Twitter length is fine
- But says nothing of substance

**Criterion 6 (Tone):** FAILS
- "Sincerely apologize for any inconvenience" is corporate template language
- No human emotion
- Sounds like it was written by Legal department, not a person

**Overall:** This apology would make customers more angry. It's defensive, vague, and offers nothing concrete. Twitter would roast us.

---

### Refined Version

**Tweet 1/4:**

We messed up. Our site was down for 4 hours during Black Friday. If you were trying to shop with us today, we let you down. I'm sorry. (Thread with what happened, what we're doing about it, and how we'll make it right.)

— Alex Chen, CEO

**Tweet 2/4:**

What happened: We deployed a database update this morning that had a bug. It caused a cascading failure across our checkout system. Our team caught it at 10:15am, but rolling back took until 2pm. This is on us.

**Tweet 3/4:**

What we're doing:
- All Black Friday deals extended through Sunday (full 72 hours)
- If your cart was lost, email us at blackfriday@company.com with your email - we'll recreate it + add 20% off
- We're reviewing our deployment process to prevent this

**Tweet 4/4:**

Black Friday is supposed to be about great deals, not website errors. We took that away from you today. The 20% discount is the least we can do. Thank you to everyone who waited it out. We'll do better.

— Alex

---

### Why This Works (Meta-Analysis)

**Empathy:**
- "We let you down" acknowledges emotional impact
- "Took that away from you" shows understanding of what was lost
- CEO personally signs it (shows accountability at top)

**Transparency:**
- Explains technical cause in simple terms (database bug)
- Timeline given (10:15am caught, 2pm fixed)
- Honest: "This is on us" (active voice, ownership)

**Accountability:**
- CEO name attached (not anonymous corporate account)
- "We messed up" is plain language, not corporate euphemism
- No passive voice, no deflection

**Action:**
- Concrete compensation: Deals extended + 20% off
- Easy path for lost carts (email, they'll fix it)
- Specific change: reviewing deployment process

**Brevity:**
- 4 tweets, easily scannable
- Each tweet has one clear point
- Total thread: ~100 words (Twitter-friendly)

**Tone:**
- "We messed up" is human, not corporate
- CEO voice makes it personal
- Balances professional with authentic

This apology likely turns angry customers into "okay, mistakes happen, at least they owned it and made it right" customers.
```

---

### **Example 3: Screenwriter (Dialogue Subtext)**

**Use Case:** Improving "on the nose" dialogue to add subtext.

```markdown
## SYSTEM
You are a Script Doctor specializing in dialogue.
You know that great dialogue is about what's NOT said.
Use Draft-Critique-Refine to polish this scene.

## TASK
Rewrite this dialogue to add emotional subtext.

## SCENE CONTEXT
Genre: Drama
Setup: Emma just discovered her husband David had an affair. They're in their kitchen. She confronted him earlier, and he admitted it. Now it's 24 hours later, and they're avoiding the topic.

Current Dialogue (This is what they SHOULDN'T say):
EMMA
I'm still very angry at you for cheating on me.

DAVID
I know. I'm sorry. It was a mistake. I love you.

EMMA
I don't know if I can trust you anymore.

DAVID
I understand. I'll do whatever it takes to earn your trust back.

## QUALITY CRITERIA

1. **Subtext**: Characters talk AROUND the issue, not directly at it
2. **Behavioral**: Show emotion through action, not declaration
3. **Conflict Avoidance**: Both want to say it but can't
4. **Specificity**: Use concrete objects/tasks, not abstract feelings
5. **Cinematic**: Visual and engaging, not talking heads
6. **Emotional Truth**: Feels real, not soap opera

## PROCESS
Draft -> Critique -> Refine (focus on making unspoken pain visible)


**Expected Output:**

### Draft Version

INT. KITCHEN - MORNING

EMMA makes coffee. DAVID enters.

DAVID
Coffee smells good.

EMMA
(not looking at him)
There's enough for two.

DAVID sits. Long pause.

DAVID
I was thinking... maybe we could talk about—

EMMA
I need to pick up groceries. Do you need anything?

DAVID
Emma, please. Can we just talk about what happened?

EMMA
There's nothing to talk about. You made your choice.

She leaves the room.

---

### Critique

**Criterion 1 (Subtext):** PARTIAL PASS
- Good: They're avoiding the topic initially
- Bad: David says "talk about what happened" (too direct, breaks the avoidance)
- Bad: Emma's last line is declarative (states the obvious)

**Criterion 2 (Behavioral):** PARTIAL PASS
- Good: Emma doesn't look at him (body language)
- Bad: Not enough physical action showing the tension
- Missing: What are they doing with their hands? Objects?

**Criterion 3 (Conflict Avoidance):** FAILS
- David breaks the avoidance too early (line 4)
- Real people in this situation would dance around it longer
- No small talk as shield

**Criterion 4 (Specificity):** FAILS
- "Groceries" is generic
- Coffee is generic
- No specific objects that carry emotional weight

**Criterion 5 (Cinematic):** PARTIAL PASS
- Some visual elements (coffee, leaving room)
- But mostly talking heads
- Missing: props, business, physical space dynamics

**Criterion 6 (Emotional Truth):** PARTIAL PASS
- Feels a bit TV-movie
- Real couples in crisis often talk about mundane things to avoid the elephant

**Overall:** Too on-the-nose at the end. Needs more layers.
```

---

### Refined Version

```markdown
INT. KITCHEN - MORNING

EMMA at the sink, aggressively washing last night's dishes. Scrubbing harder than necessary. DAVID enters, hesitates in the doorway.

DAVID
(quiet)
You're up early.

EMMA doesn't respond. Keeps scrubbing. DAVID pours coffee from the pot. Notices it's burnt. Doesn't mention it.

DAVID (CONT'D)
I can finish those.

EMMA
I've got it.

She scrubs the same plate she's been scrubbing. David sees this.

DAVID
(carefully)
Did you sleep?

EMMA
(still not looking at him)
Some.

Beat. David sits at the table. Emma SLAMS a plate into the drying rack. It doesn't break, but almost.

DAVID
Emma—

EMMA
The garbage disposal is broken again.

DAVID
I'll call the plumber.

EMMA
(sharp)
You said that last week.

DAVID
I'll do it today.

EMMA  finally turns to face him.

EMMA
Will you?

They hold eye contact. The question isn't about the plumber.

DAVID
(quietly)
Yes.

Beat. Emma turns back to the sink.

EMMA
I'm going to my mother's for a few days.

DAVID
(defeated)
Okay.

EMMA
She doesn't know. I told her I just need space.

DAVID nods. Doesn't trust himself to speak.

EMMA (CONT'D)
(back to dishes)
Can you feed the cat?

DAVID
Of course.

Silence. Emma scrubs. David drinks burnt coffee.

END SCENE

---
```

### Why This Refinement Works

**Subtext:**

- Every line is about the affair without mentioning it
- "Did you sleep?" = Do you hate me?
- "The garbage disposal is broken" = You broke us
- "Will you?" = Can I believe anything you say?

**Behavioral:**

- Scrubbing dishes aggressively = displaced anger
- Slamming plate = controlled violence
- Burnt coffee he drinks anyway = self-punishment
- Eye contact moment = the real conversation

**Conflict Avoidance:**

- They talk about plumber, cat, mother—anything but THE thing
- David starts to say her name, she deflects to appliances
- "She doesn't know" = Emma's protecting herself

**Specificity:**

- Broken garbage disposal = broken marriage
- Same plate scrubbed repeatedly = obsessive, can't move on
- Going to mother's = leaving, but temporary (hope?)

**Cinematic:**

- Physical action throughout (dishwashing, coffee pouring)
- Space dynamics (doorway hesitation, not looking, eye contact)
- Objects carry weight (burnt coffee, slammed plate)

**Emotional Truth:**

- Couples in crisis fixate on small broken things (disposal, plumber)
- Avoidance through mundane tasks is realistic
- "Can you feed the cat?" = testing if he'll be reliable

Every line has surface meaning and subtext. Audience feels the pain without it being stated.

### **Best Practices for Self-Reflection**

1. **Define Specific Quality Criteria**
    - Not: "Make it better"
    - Instead: "Must be actionable, balanced, objective, growth-oriented"

2. **Critique Against Each Criterion Separately**
    - Forces thoroughness
    - Prevents "generally okay" assessment

3. **Be Harsh in Critique**
    - The critique step should find real problems
    - If critique says "all good," you didn't look hard enough

4. **Reference Specific Lines in Critique**
    - Not: "Tone is off"
    - Instead: "Line 3: 'You must improve' is accusatory"

5. **Verify Refinement Addressed Critique**
    - After refining, check: Did we fix the identified problems?

---

### **Common Mistakes**

**Mistake 1: Vague Quality Criteria**

```
Bad: "Make it sound professional"
Good: "Must use SBI model, avoid subjective labels, include 2 positives per 1 negative"

```

**Mistake 2: Soft-Ball Critique**

```
Bad Critique: "This is pretty good, just needs minor polish"
Good Critique: "Criterion 3 FAILS: Uses 'rude' which is subjective interpretation, not observable behavior"
```

**Mistake 3: Refine Without Addressing Critique**

```
Bad: Refined version has same problems
Good: Each critique point gets specific fix in refinement
```

---

### **Key Takeaways**

* Self-Reflection implements Draft -> Critique -> Refine loop for quality control
* Define explicit quality criteria before drafting (prevents moving goalposts)
* Critique should be harsh and specific, referencing exact problems
* Refinement must address every critique point systematically
* Higher token cost but essential for sensitive/important communications
* Use when quality > speed, and first draft isn't good enough

---

**This completes the core prompting techniques.** You now have a comprehensive toolkit from Zero-Shot basics to advanced Graph of Thoughts and Self-Reflection patterns.

## **Chapter 9: Essential Short Patterns**

These are specific, high-utility patterns that solve distinct problems. Use them for specialized tasks like data extraction, storytelling, creative transitions, and autonomous agent behaviors.

---

### **9.1 Pattern A: The Narrative Bridge (Story/Style)**

#### **What Is It?**

The Narrative Bridge pattern forces the LLM to connect two seemingly disconnected concepts, tones, or emotional states in a smooth, natural transition. Instead of abrupt cuts, it creates storytelling flow that feels inevitable and organic.

#### **Intuitive Explanation**

Think of this like a cinematographer planning a seamless tracking shot that transitions from a bright comedy to a dark thriller without cutting. The LLM acts as a bridge architect, ensuring each narrative step logically leads to the next, even when the start and end points are radically different.

**Key Insight:** By constraining the model to connect A -> B smoothly, you force it to think creatively about intermediate states, metaphors, or pivots that make the transition feel earned.

#### **When to Use This Technique**

- **Screenwriting:** Transitioning between emotional beats (comedy to horror, romance to action)
- **Marketing:** Creating ad narratives that shift from problem (pain) to solution (relief)
- **Copywriting:** Building persuasive flow from attention-grabbing hook to call-to-action
- **Brand Storytelling:** Connecting product features to emotional benefits

#### **Why Use This Technique**

- **Prevents Jarring Transitions:** Ensures smooth emotional/tonal shifts
- **Creates Memorable Moments:** Unexpected yet natural connections stick with audiences
- **Maintains Engagement:** Keeps readers/viewers invested through the transition
- **Tests Creative Constraints:** Forces creative problem-solving within limitations

---

#### **Prompt Template**

```markdown
## SYSTEM
You are a Master Storyteller specializing in seamless narrative transitions.

## TASK
Connect Concept A ({{START}}) to Concept B ({{END}}) using the specified tone ({{TONE}}).

## CONSTRAINTS
- The transition must feel natural and inevitable
- Each intermediate step should logically follow the previous one
- {{ADDITIONAL_CONSTRAINTS}}

## OUTPUT STRUCTURE
1. Opening (Concept A)
2. Transition Bridge (3-5 intermediate steps)
3. Resolution (Concept B)

## START CONCEPT
{{START}}

## END CONCEPT
{{END}}

## TONE
{{TONE}}
```

---

#### **Example 1: Screenwriter (Tone Shift)**

```markdown
## SYSTEM
You are a Script Doctor specializing in tonal transitions for psychological thrillers.

## TASK
Rewrite this comedic scene opener to end on a terrifying note.

## START CONCEPT
Two circus clowns slipping on banana peels in a bright, colorful tent. Children laughing.

## END CONCEPT
The discovery of a dead body hidden beneath the circus stage.

## CONSTRAINTS
- Do not cut the camera. It must be one continuous tracking shot
- The tone shift should happen gradually over 2-3 minutes of screen time
- Use environmental details (lighting, sound, props) to signal the shift

## TONE PROGRESSION
Comedy -> Unease -> Suspense -> Horror
```

**Expected Output:**
A detailed scene description showing how the camera follows a clown through the tent, with laughter slowly fading, lighting dimming, music distorting, until the clown stumbles through a trap door and discovers the body.

---

#### **Example 2: Marketing Manager (Problem-to-Solution Arc)**

```markdown
## SYSTEM
You are a Brand Storyteller for a productivity SaaS company.

## TASK
Create a 60-second video script that transitions from chaotic work-life to serene productivity.

## START CONCEPT
A stressed professional drowning in emails, missed deadlines, and chaos.

## END CONCEPT
The same person calmly finishing their workday early, spending time with family.

## TONE PROGRESSION
Anxiety -> Discovery -> Hope -> Satisfaction

## CONSTRAINTS
- Must introduce the product naturally in the middle transition
- Use visual metaphors (e.g., tangled strings becoming organized threads)
- Total word count: 150 words maximum
```

---

#### **Example 3: Screenwriter (Genre Mashup)**

```markdown
## SYSTEM
You are a Creative Director pitching a genre-bending TV series.

## TASK
Describe the pilot episode arc that transitions from romantic comedy to science fiction.

## START CONCEPT
Two strangers meet-cute at a coffee shop. Classic rom-com banter.

## END CONCEPT
They discover they are from parallel universes and their meeting could collapse reality.

## TONE PROGRESSION
Light-hearted Romance -> Curiosity -> Mystery -> Sci-Fi Thriller

## CONSTRAINTS
- The transition should happen in Act 2
- Use foreshadowing in Act 1 (subtle glitches in reality)
- Maintain romantic chemistry even as stakes escalate
```

---

### **9.2 Pattern B: The Strict JSON Parser (Data)**

#### **What Is It?**

The Strict JSON Parser pattern transforms the LLM from a conversational assistant into a deterministic data extraction API. It outputs only pure, valid JSON without any explanatory text, Markdown formatting, or preambles.

#### **Intuitive Explanation**

Imagine you're building a REST API endpoint. You don't want your `/api/user` endpoint to return:

```
Here's the user data you requested:
```json
{"name": "Alice"}
```

```
You want it to return **only**:
```json
{"name": "Alice"}
```

This pattern enforces that discipline on the LLM, making it behave like a pure function: `text_input -> JSON_output`.

#### **When to Use This Technique**

- **Backend Engineering:** Parsing logs, extracting structured data from unstructured text
- **Data Pipelines:** ETL processes requiring consistent JSON schemas
- **Machine Learning:** Preparing training data or feature extraction
- **API Integration:** When LLM output feeds directly into other systems
- **DevOps:** Log analysis, error reporting, monitoring alerts

#### **Why Use This Technique**

- **Programmatic Parsing:** Output can be directly parsed with `JSON.parse()` or `json.loads()`
- **No Cleanup Required:** Eliminates need to strip Markdown fences or explanatory text
- **Consistent Schema:** Enforces strict data contracts for downstream systems
- **Pipeline Integration:** Seamlessly integrates into automated data processing workflows
- **Reliability:** Reduces edge cases where model adds extra commentary

---

#### **Prompt Template**

```markdown
## SYSTEM
You are a Data Extraction Engine. 
Output ONLY valid JSON. 
Do NOT include:
- Markdown code fences (```json)
- Explanatory text before or after JSON
- Comments or annotations
- Pretty-printing line breaks

## TASK
Extract {{DATA_TYPE}} from the provided text.

## INPUT
{{INPUT_TEXT}}

## OUTPUT SCHEMA
{{JSON_SCHEMA}}

## VALIDATION RULES
- Every field in the schema is required
- Use null for missing data
- Dates must be in ISO8601 format
- Numbers must be numeric types, not strings
```

---

#### **Example 1: Engineering (Log Parsing)**

```markdown
## SYSTEM
You are a Log Parser. Output strictly valid JSON with no additional text.

## INPUT
"2023-10-25 10:00:01 [ERROR] User 555 failed login: Invalid Password. IP: 192.168.1.10"

## OUTPUT SCHEMA
{
  "timestamp": "ISO8601 string",
  "level": "ERROR|WARN|INFO",
  "user_id": "number or null",
  "event": "string",
  "ip_address": "string or null",
  "reason": "string"
}
```

**Expected Output (pure JSON, no formatting):**

```json
{"timestamp":"2023-10-25T10:00:01Z","level":"ERROR","user_id":555,"event":"login_failed","ip_address":"192.168.1.10","reason":"Invalid Password"}
```

---

#### **Example 2: DevOps (Error Report Extraction)**

```markdown
## SYSTEM
You are an Error Report Extractor for incident management systems.
Output only valid JSON.

## TASK
Parse the stack trace and extract key error information.

## INPUT
"""
Exception in thread "main" java.lang.NullPointerException: Cannot invoke "String.length()" because "text" is null
    at com.example.Parser.validate(Parser.java:42)
    at com.example.Main.processData(Main.java:15)
    at com.example.Main.main(Main.java:8)
"""

## OUTPUT SCHEMA
{
  "error_class": "string",
  "error_message": "string",
  "root_file": "string",
  "root_line": "number",
  "root_method": "string"
}
```

**Expected Output:**

```json
{"error_class":"java.lang.NullPointerException","error_message":"Cannot invoke \"String.length()\" because \"text\" is null","root_file":"Parser.java","root_line":42,"root_method":"validate"}
```

---

#### **Example 3: Marketing Manager (Sentiment Analysis)**

```markdown
## SYSTEM
You are a Customer Feedback Analyzer.
Output only valid JSON.

## TASK
Analyze the sentiment and extract key themes from customer review.

## INPUT
"I absolutely love the design and the battery life is amazing! However, the customer support was slow to respond and it took a week to get my issue resolved. Overall, I'd recommend it to friends."

## OUTPUT SCHEMA
{
  "overall_sentiment": "positive|neutral|negative",
  "sentiment_score": "number between -1.0 and 1.0",
  "positive_aspects": ["array of strings"],
  "negative_aspects": ["array of strings"],
  "would_recommend": "boolean"
}
```

**Expected Output:**

```json
{"overall_sentiment":"positive","sentiment_score":0.6,"positive_aspects":["design","battery life"],"negative_aspects":["slow customer support response"],"would_recommend":true}
```

---

#### **Example 4: Engineering Manager (Resume Parsing)**

```markdown
## SYSTEM
You are a Resume Parser for an Applicant Tracking System (ATS).
Output only valid JSON.

## INPUT
"""
Jane Doe
Senior Software Engineer
jane.doe@email.com | LinkedIn: linkedin.com/in/janedoe

Experience:
- Google (2020-2023): Led backend team, scaled services to 10M users
- Startup Inc (2018-2020): Full-stack developer, React & Node.js

Skills: Python, Go, Kubernetes, AWS, React
Education: BS Computer Science, MIT (2018)
"""

## OUTPUT SCHEMA
{
  "name": "string",
  "email": "string",
  "phone": "string or null",
  "current_title": "string or null",
  "years_experience": "number",
  "skills": ["array of strings"],
  "companies": [{"name": "string", "years": "number"}],
  "education": {"degree": "string", "institution": "string", "year": "number"}
}
```

---

### **9.3 Pattern C: The ReAct Skeleton (Reason + Act)**

#### **What Is It?**

ReAct (Reasoning + Acting) is the foundational pattern for autonomous AI agents. The model alternates between **thinking** (reasoning about what to do next) and **acting** (executing tools/commands), creating an observable loop that can be debugged and controlled.

#### **Intuitive Explanation**

Think of ReAct as the "show your work" methodology from math class, but for AI agents. Instead of jumping straight to an answer, the model:

1. **Thinks:** "What information do I need?"
2. **Acts:** Calls a tool/API to get that information
3. **Observes:** Sees the result
4. **Repeats:** Until it has enough to answer

This makes the agent's decision-making **transparent** and **debuggable**—you can see exactly why it chose to take each action.

**Mental Model:** It's like pair programming with an LLM where it narrates its thought process before writing each line of code.

#### **When to Use This Technique**

- **DevOps:** Automated troubleshooting, incident response, log analysis
- **Research Agents:** Multi-step information gathering (e.g., market research, competitor analysis)
- **Customer Support Bots:** Diagnosing issues through sequential queries
- **Data Analysis:** Exploratory data analysis requiring multiple tool calls
- **Testing & QA:** Automated bug reproduction and root cause analysis

#### **Why Use This Technique**

- **Transparency:** Every decision is visible and auditable
- **Debuggability:** You can see where reasoning went wrong
- **Modularity:** Easy to swap out tools or modify reasoning steps
- **Controllability:** Can inject human approval gates at any Act step
- **Error Recovery:** Failed actions can be retried with updated reasoning
- **Multi-Step Tasks:** Handles complex workflows requiring multiple actions
- **Foundation for Agents:** Core pattern used in LangChain, AutoGPT, BabyAGI

---

#### **Prompt Template**

```markdown
## SYSTEM
You are an autonomous {{AGENT_ROLE}}.
You have access to the following tools: {{TOOL_LIST}}

## FORMAT
Use this exact format for every step:

**Thought:** [Describe what you need to know or do next]
**Action:** [TOOL_NAME] (parameter)
**Observation:** [Result from the tool - this will be provided by the system]

Repeat this Thought -> Action -> Observation loop until you can answer.

**Final Answer:** [Your conclusion based on observations]

## RULES
1. Always think before acting
2. Use one tool per action
3. Wait for observation before next thought
4. If a tool fails, think about an alternative approach
5. Provide final answer only when you have sufficient information

## QUESTION
{{USER_QUESTION}}

## AVAILABLE TOOLS
{{TOOL_DESCRIPTIONS}}
```

---

#### **Example 1: DevOps (Kubernetes Debugging Agent)**

```markdown
## SYSTEM
You are a Kubernetes Debugging Agent for production systems.

## AVAILABLE TOOLS
- kubectl_get: Get resource status (e.g., "kubectl get pods -n payments")
- kubectl_logs: Fetch pod logs (e.g., "kubectl logs pod-name --previous")
- kubectl_describe: Detailed resource info (e.g., "kubectl describe pod pod-name")
- search_docs: Search internal runbooks

## QUESTION
Why is the 'payments-api' service returning 503 errors to users?

## FORMAT
**Thought:** [Your reasoning]
**Action:** [TOOL] (parameters)
**Observation:** [Result - will be provided]
...
**Final Answer:** [Root cause and recommended fix]
```

**Expected Agent Flow:**

```
**Thought:** I need to check if the payments-api pods are running.
**Action:** kubectl_get (pods -n payments)
**Observation:** 
NAME                  READY   STATUS             RESTARTS
payments-api-7d4f9    0/1     CrashLoopBackOff   5
payments-api-n82k1    0/1     CrashLoopBackOff   5

**Thought:** The pods are crash-looping. I need to check the logs to see why.
**Action:** kubectl_logs (payments-api-7d4f9 --previous)
**Observation:** 
[ERROR] 2023-10-25 10:15:33 - Failed to connect to database: Connection timeout after 5000ms
[ERROR] 2023-10-25 10:15:33 - Host: postgres-primary.db.svc.cluster.local:5432

**Thought:** The app can't connect to the database. Let me verify the database service is running.
**Action:** kubectl_get (pods -n db)
**Observation:**
NAME                READY   STATUS    RESTARTS
postgres-primary    1/1     Running   0

**Thought:** Database pod is running. This might be a networking or DNS issue. Let me check the service endpoints.
**Action:** kubectl_describe (service postgres-primary -n db)
**Observation:**
Name:              postgres-primary
Namespace:         db
Selector:          app=postgres,role=primary
Endpoints:         <none>

**Thought:** The service has no endpoints! The selector might not match the pod labels.
**Final Answer:** 
Root Cause: The postgres-primary service has no endpoints because the selector doesn't match the running pods. This causes payments-api to fail connecting to the database.

Recommended Fix:
1. Check pod labels: kubectl get pods -n db --show-labels
2. Update service selector to match actual pod labels
3. Verify endpoints appear: kubectl get endpoints postgres-primary -n db
```

---

#### **Example 2: Research Agent (Competitive Analysis)**

```markdown
## SYSTEM
You are a Market Research Agent for a SaaS startup.

## AVAILABLE TOOLS
- web_search: Search the web (e.g., "web_search('competitor pricing 2024')")
- scrape_page: Extract content from URL
- analyze_sentiment: Analyze customer reviews
- calculate: Perform calculations

## QUESTION
What is the average pricing of the top 3 project management tools similar to our product, and how do customers rate their value for money?

## OUTPUT
Provide final answer with:
1. Competitor pricing comparison table
2. Value-for-money sentiment summary
3. Recommended pricing strategy
```

**Expected Flow:**

```
**Thought:** I need to identify the top 3 project management tools first.
**Action:** web_search ("top project management software 2024")
**Observation:** Asana, Monday.com, and ClickUp are mentioned as leaders.

**Thought:** Now I need their pricing information.
**Action:** web_search ("Asana pricing tiers 2024")
**Observation:** Basic: $10.99/user/month, Premium: $24.99/user/month

**Thought:** Let me get Monday.com pricing.
**Action:** web_search ("Monday.com pricing")
**Observation:** Basic: $9/user/month, Standard: $12/user/month, Pro: $19/user/month

**Thought:** And ClickUp pricing.
**Action:** web_search ("ClickUp pricing tiers")
**Observation:** Unlimited: $7/user/month, Business: $12/user/month, Enterprise: custom

**Thought:** Now I'll calculate the average for mid-tier plans.
**Action:** calculate ((24.99 + 12 + 12) / 3)
**Observation:** 16.33

**Thought:** I need customer sentiment on value for money.
**Action:** web_search ("Asana Monday ClickUp customer reviews value pricing")
**Observation:** [Reviews indicate users find ClickUp best value, Monday.com overpriced for small teams]

**Final Answer:**

COMPETITOR PRICING COMPARISON:
| Tool       | Entry  | Mid-Tier | Premium |
|------------|--------|----------|---------|
| Asana      | $10.99 | $24.99   | N/A     |
| Monday.com | $9     | $12      | $19     |
| ClickUp    | $7     | $12      | Custom  |

Average Mid-Tier: $16.33/user/month

VALUE SENTIMENT:
- ClickUp: Rated "excellent value" - feature-rich at low price point
- Monday.com: Mixed - seen as expensive for small teams, justified for enterprises
- Asana: Premium tier perceived as overpriced vs. competitors

RECOMMENDED STRATEGY:
Price at $14-15/user/month (below average but above budget tier) to position as "premium features at mid-market price." Emphasize features comparable to Asana Premium at 40% lower cost.
```

---

#### **Example 3: Engineering Manager (Incident Post-Mortem Agent)**

```markdown
## SYSTEM
You are a Post-Mortem Analysis Agent.

## AVAILABLE TOOLS
- query_logs: Search application logs by timeframe and keywords
- query_metrics: Get system metrics (CPU, memory, latency, error rate)
- get_deployment_history: List recent deployments
- search_alerts: Find triggered alerts in timeframe

## QUESTION
Generate a post-mortem for the API latency spike that occurred on 2023-10-25 between 14:00-15:00 UTC.

## REQUIRED OUTPUT
1. Timeline of events
2. Root cause
3. Impact assessment
4. Action items to prevent recurrence
```

**Expected Flow:**

```
**Thought:** I need to establish the timeline by checking when alerts fired.
**Action:** search_alerts (timeframe: "2023-10-25 14:00-15:00 UTC")
**Observation:** 
14:03 - High API Latency Alert (p95 latency: 2400ms, threshold: 500ms)
14:12 - Database Connection Pool Exhaustion Alert
14:47 - Alert resolved (p95 latency: 320ms)

**Thought:** Database connection pool exhaustion might be the root cause. Let me check deployments.
**Action:** get_deployment_history (since: "2023-10-25 13:00")
**Observation:**
13:45 - deployment: api-service v2.3.1 (changed database query batching logic)

**Thought:** A deployment 15 minutes before the incident is suspicious. Let me check metrics.
**Action:** query_metrics (service: "api-service", metric: "db_connections", timeframe: "14:00-15:00")
**Observation:**
14:00: 50 connections (normal)
14:05: 98 connections (near max pool size of 100)
14:10: 100 connections (pool exhausted)
14:30: Engineers rolled back deployment
14:47: 45 connections (returned to normal)

**Thought:** Let me verify what changed in the query batching logic.
**Action:** query_logs (keywords: "query batch", timeframe: "14:00-14:15")
**Observation:**
[ERROR] 14:05:11 - Batch size exceeded max. Falling back to individual queries
[WARN] 14:05:23 - Query timeout: 30s exceeded for user_data fetch

**Final Answer:**

POST-MORTEM: API Latency Incident (2023-10-25)

TIMELINE:
- 13:45 UTC: Deployed api-service v2.3.1 with query batching changes
- 14:03 UTC: High latency alert triggered (p95: 2400ms vs 500ms threshold)
- 14:05 UTC: Batch size errors in logs; system falling back to individual queries
- 14:12 UTC: Database connection pool exhausted (100/100 connections in use)
- 14:30 UTC: Engineering team initiated rollback
- 14:47 UTC: Service returned to normal latency

ROOT CAUSE:
The new query batching logic in v2.3.1 had a bug where batch size limits were not enforced, causing the system to fall back to individual queries. This created a 20x increase in database calls, exhausting the connection pool and causing cascading latency.

IMPACT:
- Duration: 44 minutes
- Affected: 100% of API traffic
- User Impact: Slow page loads (2-3 second delays)
- No data loss or security impact

ACTION ITEMS:
1. [P0] Add integration tests for query batching with batch size limits
2. [P0] Implement connection pool monitoring with pre-emptive alerts at 80% capacity
3. [P1] Add staged rollouts (canary 10% -> 50% -> 100%) for database-touching changes
4. [P1] Document rollback procedures to reduce incident response time (30min was too slow)
```

---

#### **Key Takeaways for Chapter 9**

| Pattern                | Best For                            | Output Type               | Primary Benefit              |
| ---------------------- | ----------------------------------- | ------------------------- | ---------------------------- |
| **Narrative Bridge**   | Creative transitions, storytelling  | Prose/Script              | Smooth tonal shifts          |
| **Strict JSON Parser** | Data extraction, APIs, automation   | Pure JSON                 | Programmatic parsing         |
| **ReAct (Reason+Act)** | Autonomous agents, multi-step tasks | Structured reasoning loop | Transparency & debuggability |

**When to combine patterns:**

- Use **ReAct** + **Strict JSON** for agents that need to output structured data at each step
- Use **Narrative Bridge** + **Few-Shot** (Chapter 4) to teach specific transition styles by example
- Use **ReAct** + **Self-Reflection** (Chapter 8) for self-correcting agents that critique their own actions

## **Chapter 10: Practice Workshop**

Practice these drills to master each technique. Copy the template from the previous chapters and apply it to these scenarios.

### **10.1 Few-Shot Drills**

1. **\[Screenwriting\] Genre Style Transfer:**  
    * *Task:* Create a Few-Shot prompt that takes a neutral line like "Hello, how are you?" and transforms it into 3 genres: Noir ("What's eating you, kid?"), Fantasy ("Greetings, traveler"), and Cyberpunk ("Status report?").  
2. **\[Engineering\] Log Parsing:**  
    * *Task:* Build a Few-Shot prompt to convert raw, multi-line Java stack traces into a single-line JSON object containing {"timestamp": "", "error\_class": "", "root\_cause": ""}.  
3. **\[Marketing\] Feature-to-Benefit:**  
    * *Task:* Feed the model 3 examples of converting technical specs (e.g., "4000mAh battery") into lifestyle benefits (e.g., "Power that lasts all weekend"). Ask it to convert a list of SaaS dashboard features.  
4. **\[Screenwriting\] Prop Extraction:**  
    * *Task:* Provide examples of a script scene input and a bulleted output list of every physical prop mentioned. Test it on a complex action scene.  
5. **\[Engineering\] Git Commit Formatting:**  
    * *Task:* Teach the model the "Conventional Commits" standard (e.g., feat:, fix:, chore:) with 5 examples. Feed it a vague sentence like "I changed the button color" and ensure it outputs style(ui): update primary button color.

### **10.2 Chain of Thought Drills**

1. **\[Marketing\] Attribution Logic:**  
    * *Task:* A user clicks a Facebook Ad, then a YouTube Ad, then an Email Link, then buys. Ask the model to reason step-by-step through "Linear" vs "Last-Click" attribution to determine which channel gets credit.  
2. **\[Engineering\] Memory Leak Detective:**  
    * *Task:* Provide a scenario: "Server memory usage grows by 5% every hour but drops after restart." Ask the model to reason through potential causes (Global variables? Unclosed DB connections? Caching?) before suggesting a fix.  
3. **\[Screenwriting\] Timeline Consistency:**  
    * *Task:* Scene A is in London (Day). Scene B is in New York (Day, Same Date). Ask the model to reason through time zones and flight durations to check if this transition is logically possible.  
4. **\[Engineering\] Database Sharding Strategy:**  
    * *Task:* You have 50TB of data. Ask the model to reason through sharding by UserID vs TenantID vs GeoLocation, listing the pros/cons of query performance for each before making a choice.  
5. **\[Marketing\] ROI Significance:**  
    * *Task:* Campaign A has a 5% conversion rate (100 visitors). Campaign B has a 4% conversion rate (10,000 visitors). Ask the model to reason through statistical significance to decide which campaign is actually performing better reliably.

### **10.3 Tree of Thoughts Drills**

1. **\[Screenwriting\] "Save the Cat" Brainstorming:**  
    * *Task:* Generate 3 branches for how an unlikable anti-hero can show kindness (Save the Cat moment) early in the film. Evaluate each for "Audience Sympathy" vs "Character Consistency".  
2. **\[Engineering\] Legacy Migration Strategy:**  
    * *Task:* You need to replace a 10-year-old monolith. Generate 3 branches: (A) Big Bang Rewrite, (B) Parallel Run, (C) Strangler Fig Pattern. Evaluate risks and costs for each.  
3. **\[Marketing\] Viral Campaign Angle:**  
    * *Task:* You are selling "Life Insurance". Generate 3 tonal branches: (A) Humor/Dark Comedy, (B) Deeply Emotional/Tearjerker, (C) Data-Driven/Logical. Evaluate which is most likely to go viral on TikTok.  
4. **\[Engineering\] API Versioning:**  
    * *Task:* Choose an API versioning strategy. Branches: (A) URI Versioning (/v1/), (B) Header Versioning, (C) Query Parameter. Evaluate based on "Browser Caching" and "Developer DX".  
5. **\[Screenwriting\] Title Generation:**  
    * *Task:* Generate 3 metaphorical titles for a movie about a chef losing his sense of taste. Evaluate them on "Mystery", "Marketability", and "Thematic Resonance".

### **10.4 Graph of Thoughts Drills**

1. **\[Engineering\] Microservices Blast Radius:**  
    * *Task:* Map a dependency graph where Service A calls Service B and C. Service B calls D. If D fails, map how the error propagates back to A and which fallback mechanisms (Circuit Breakers) should trigger at each node.  
2. **\[Marketing\] Content Repurposing Engine:**  
    * *Task:* Node A is a Webinar. Node B is a Blog Post. Node C is a LinkedIn Thread. Node D is a Short Video. Map the workflow edges showing how content flows from A to B/C/D and what elements are reused (e.g., "Audio from A becomes script for D").  
3. **\[Screenwriting\] Character Arc Intersections:**  
    * *Task:* You have 4 characters. Map their emotional arcs as nodes. Identify the specific scenes (Edges) where their arcs must intersect to create conflict. Ensure Character A's high point coincides with Character B's low point.  
4. **\[Engineering\] Cloud Cost Optimization:**  
    * *Task:* Nodes are Compute, Storage, and Network. Increasing Compute (Node A) might reduce Storage processing time (Node B) but increase Network egress (Node C). Use GoT to find the optimal balance point.  
5. **\[Marketing\] Event Logistics:**  
    * *Task:* Node A is Keynote Speaker. Node B is Catering. Node C is Audio/Visual. Node D is Budget. Map how a delay in Node A affects B and C, and how an upgrade in C affects D.

### **10.5 Self-Reflection Drills**

1. **\[Marketing\] Cold Email Critique:**  
    * *Task:* Draft a sales email. Then, use a persona "Ruthless CFO" to critique it for fluff, buzzwords, and lack of ROI. Rewrite the email based on the CFO's insults.  
2. **\[Engineering\] Architecture RFC Review:**  
    * *Task:* Write a proposal for a new caching layer. Then, act as a "Principal Engineer" and critique it for Single Points of Failure and Cache Invalidation strategies.  
3. **\[Screenwriting\] Dialogue Subtext Check:**  
    * *Task:* Write a scene where two lovers break up. Critique it: "Are they saying exactly what they feel?" (Bad). Rewrite it so they are arguing about whose turn it is to do the dishes, but the *subtext* is the breakup.  
4. **\[Marketing\] Landing Page Optimization:**  
    * *Task:* Draft a landing page headline. Critique it: "Is this feature-focused or benefit-focused?" "Is the Call to Action clear?" Rewrite to maximize conversion.  
5. **\[Engineering\] Code Refactoring:**  
    * *Task:* Write a complex, nested if-else function. Critique it for "Readability" and "Cyclomatic Complexity". Rewrite it using Guard Clauses or Strategy Pattern.

*End of Master Guide*