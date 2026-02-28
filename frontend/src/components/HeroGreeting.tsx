import React from 'react';

export default function HeroGreeting() {
    return (
        <div className="flex flex-col items-center justify-center text-center">
            <h1 className="text-3xl font-semibold text-origin-text mb-2">
                Good Morning, [User].
            </h1>
            <p className="text-xl text-origin-text">
                Ask a Tax Question.
            </p>
        </div>
    );
}
